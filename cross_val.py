import statistics as st

import math
from collections import defaultdict

from os.path import isfile
from os.path import join
from os.path import sep
from os import listdir


class KeyGuesser:
    def __init__(self, lb=0.02, hb=1.5, shift=0.0059):
        self.lb = lb
        self.hb = hb
        self.shift = shift
        self.models = None
        self.data = None
        self.model_size = None

    def normalize(self, a):
        r = list(filter(lambda x: self.lb < x < self.hb, a))
        r = [max(0, x - self.shift) for x in r]
        return r

    def my_gamma(self, e, v, x):
        theta = v/e
        k = e/theta
        return stats.gamma.pdf(x, a=k, scale=theta)

    def read_data(self, filename):
        with open(filename) as f:
            letters = f.readline().split(sep=') (')[1:-1]

        res = []
        for l in letters:
            try:
                res.append((l[1], -float(l[4:])))
            except:
                pass

        return res

    def read_from_dir(self, dirname):
        files = [join(dirname, f) for f in listdir(dirname) if isfile(join(dirname, f))]
        res = {}
        for f in files:
            res[f.split('.')[0].split(sep)[-1]] = self.read_data(f)
        self.data = res
        return res

    def create_model(self, data, size=None):
        times = defaultdict(list)
        for d in data[:size]:
            try:
                times[d[0]].append(d[1])
            except:
                pass

        res = {}
        for k, v in times.items():
            a = list(self.normalize(v))
            try:
                res[k] = (st.mean(a), st.variance(a))
            except:
                pass

        self.models = res
        return res

    def create_models(self, size=None):
        self.model_size = size
        res = {}
        for k, v in self.data.items():
            res[k] = self.create_model(v, size=size)
            self.models = res
        return res

    def score(self, model, data):
        res = 0
        for d in data:
            try:
                e, v = model[d[0]]
                res += math.log(self.my_gamma(e, v, d[1]))
            except:
                pass
        return res

    def clf_gamma(self, models, data):
        return max(models, key=lambda x: self.score(models[x], data))

    def clf_knn(self, models, data):
        scores = defaultdict(int)
        for l, t in data:
            try:
                scores[max(models, key=lambda x: abs(models[x][l][0] - t))] += 1
            except:
                pass
        return min(scores, key=lambda x: scores[x])

    def classify(self, models, data):
        if self.model_size < 25:
            return self.clf_gamma(models, data)
        else:
            return self.clf_knn(models, data)

    def class_sort(self, models, data):
        return sorted(models, reverse=True, key=lambda x: self.score(models[x], data))

    def cv_score(self, piece):
        start = self.model_size

        total = 0
        win = 0
        for k, v in self.data.items():
            for i in range((len(v) - start)//piece):
                test = v[start + i*piece: start + (i + 1)*piece]
                # print(test)
                cl = self.classify(self.models, test)
                if k == cl:
                    win += 1
                total += 1

        return win / total



res = []

for i in range(20, 200, 10):
    for j in range(20, 200, 10):
        cls = KeyGuesser()
        cls.read_from_dir('test_data')
        cls.create_models(size=i)
        t = cls.cv_score(j)
        res.append(t)
        print(i, j, t)


# for k, v in sorted(res.items()):
#     print(k)
#     print('len:', len(v))
#     print('mean:', st.mean(v))
#     print('median:', st.median(v))
#     if len(v) > 1:
#         print('stdev:', st.stdev(v))
#         print('var:', st.var(v))
    # means.append((k, st.mean(v)))
# plt.hist(qwe, bins=50, normed=True)
# m = st.mean(qwe)
# v = st.variance(qwe)
# plt.plot([i/100 for i in range(1, 200)], [my_gamma(m, v, i/100) for i in range(1, 200)], color='red')
# plt.show()
# print(sorted(means, key=lambda x:x[1]))
