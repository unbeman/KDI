import msvcrt
import os
from time import time

chn = int(input('Введите желаемое количество символов:'))
name = input('Введите имя:')
if os.path.isfile(name + '.txt'):
    r = input('Файл ' + name + '.txt уже существует. Введите y, чтобы добавить данные или любую букву, чтобы выйти.')
    if r != 'y':
        exit()

res = []
prev_time = time()
i = 0
while i < chn:
    if msvcrt.kbhit():
        t = time()
        i += 1
        if i % 50 == 0:
            print('entered', i, 'chars')
        c = msvcrt.getwch()
        res.append((c, prev_time - t))
        prev_time = t


if os.path.isfile(name + '.txt'):
    with open(name + '.txt', 'a') as f:
        print(*res, file=f)
else:
    with open(name + '.txt', 'w') as f:
        print(*res, file=f)