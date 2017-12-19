import statistics as st

import math
from collections import defaultdict
from os import listdir

from os.path import isfile

from os.path import join
from time import time

from os.path import sep

from getch import getch

class KeyGuesser:
    # Конструктор класса с границами и сдвигом
    def __init__(self, lb=0.02, hb=1.5, shift=0.0059):
        self.lb = lb
        self.hb = hb
        self.shift = shift
        self.models = None
        self.data = None
        self.model_size = None

    def normalize(self, a):
        r = list(filter(lambda x: self.lb < x < self.hb, a))  # отбрасываем данные больше или меньше границ
        r = [max(0, x - self.shift) for x in
             r]  # сдвигаем данные на shift влево, если появились отрицательные, заменяем на 0
        return r

    # считаем плотность распределения, зная среднее и дисперсию
    def my_gamma(self, e, v, x):
        theta = v / e
        k = e / theta  # оцениваем параметры
        return x ** (k - 1) * math.e ** (-x / theta) / theta ** k / math.gamma(k)  # считаем

    def read_data(self, filename):
        with open(filename) as f:  # читаем данные из файла
            letters = f.readline().split(sep=') (')[1:-1]

        res = []
        for l in letters:
            try:  # вытаскиваем из строки букву и время
                res.append((l[1], -float(l[4:])))
            except:
                pass

        return res

    def read_from_dir(self, dirname):
        files = [join(dirname, f) for f in listdir(dirname) if
                 isfile(join(dirname, f))]  # получаем список файлов в папке
        res = {}
        for f in files:
            res[f.split('.')[0].split(sep)[-1]] = self.read_data(f)  # сохраняем с нужным именем в словарь
        self.data = res
        return res

    def create_model(self, data, size=None):
        times = defaultdict(list)
        for d in data[:size]:
            try:
                times[d[0]].append(d[1])  # переделываем данные в словарь массивов
            except:
                pass

        res = {}
        for k, v in times.items():
            a = list(self.normalize(v))  # нормализуем
            try:
                res[k] = (st.mean(a), st.variance(a))  # считаем среднееи дисперсию для каждого массива в словаре
            except:
                pass

        self.models = res
        return res

    def create_models(self, size=None):
        self.model_size = size or float("+inf")
        res = {}
        for k, v in self.data.items():
            res[k] = self.create_model(v, size=size)  # создаем словарь моделей от имен
            self.models = res
        return res

    # считаем насколько данные соответствуют модели
    def score(self, model, data):
        res = 0
        for d in data:
            try:
                e, v = model[d[0]]
                res += math.log(self.my_gamma(e, v, d[1]))  # складывем логарифмы вероятности
            except:
                pass
        return res

    # классифицируем с использованием гамма функции
    def clf_gamma(self, models, data):
        return max(models, key=lambda x: self.score(models[x], data))

    # классифицируем с плюсиками
    def clf_knn(self, models, data):
        scores = defaultdict(int)
        for l, t in data:
            try:
                scores[max(models, key=lambda x: abs(models[x][l][0] - t))] += 1
            except:
                pass
        return min(scores, key=lambda x: scores[x])

    # выбиаем классификацию
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
            for i in range((len(v) - start) // piece):
                test = v[start + i * piece: start + (i + 1) * piece]
                # print(test)
                cl = self.classify(self.models, test)
                if k == cl:
                    win += 1
                total += 1

        return win / total


clf = KeyGuesser()
clf.read_from_dir('data')
clf.create_models()

res = []
prev_time = time()
i = 0
while True:
        i += 1
        if i % 10 == 0:
            print(clf.classify(clf.models, res))
        c = getch()  # получить символ
        t = time()
        res.append((c, t - prev_time))  # сохранить данные
        prev_time = t
