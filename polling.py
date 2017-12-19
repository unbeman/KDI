import os
from time import time
from getch import getch

chn = int(input('Введите желаемое количество символов:'))
name = input('Введите имя:')
filename = "data/" + name + ".txt"

if os.path.isfile(filename):
    r = input('Файл ' + filename + '.txt уже существует. Введите y, чтобы добавить данные или любую букву, чтобы выйти.')
    if r != 'y':
        exit()

res = []
prev_time = time()
i = 0
while i < chn:
        c = getch()
        t = time()
        res.append((c, prev_time - t))
        prev_time = t
        
        i += 1
        if i % 50 == 0:
            print('entered', i, 'chars')

print("\n complete, ", name)

if os.path.isfile(filename):
    with open(filename, 'a') as f:
        print(*res, file=f)
else:
    with open(filename, 'w') as f:
        print(*res, file=f)

