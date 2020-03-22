from bs4 import BeautifulSoup  # pip install bs4
from urllib import request
from pulp import *  # pip install pulp
import numpy as np

pokemons = []
start_num = 0
poke_num = 890
# スクレイピング
html = request.urlopen(
    r"https://ja.wikipedia.org/wiki/%E5%85%A8%E5%9B%BD%E3%83%9D%E3%82%B1%E3%83%A2%E3%83%B3%E5%9B%B3%E9%91%91%E9%A0%86%E3%81%AE%E3%83%9D%E3%82%B1%E3%83%A2%E3%83%B3%E4%B8%80%E8%A6%A7"
)
soup = BeautifulSoup(html, features="html.parser")
tables = soup.find_all("td")
for table in tables:
    pokes = table.find_all("td")
    for i, poke in enumerate(pokes):
        if i % 2 == 1:
            if poke.string != '\xa0\n':
                pokemons.append(poke.text)
pokemons = pokemons[start_num:poke_num]
for i in range(len(pokemons)):
    if pokemons[i][-1:] == '\n':
        pokemons[i] = pokemons[i][:-1]
kw = pokemons[:]
# 処理1 記号を日本語に
kw[28] = "ニドランメス"
kw[31] = "ニドランオス"
kw[232] = "ポリゴンツー"
kw[473] = "ポリゴンゼット"
# 処理2　拗音を処理、"ー"を除去
d = {i: j for i, j in zip('ィャュョ', 'イヤユヨ')}
kw = [''.join(d.get(c, c) for c in s.rstrip('ー')) for s in kw]
with open('names.txt', 'w', encoding='UTF-8') as fo:
    for i in range(poke_num - start_num):
        fo.write(f"{kw[i]}\n")
print("Data collected")

n, r = len(kw), range(len(kw))
m = LpProblem(sense=LpMaximize)  # 数理モデル
xb = [[0 if (kw[i][-1] != kw[j][0] or i == j) else LpVariable('x%d_%d' % (i, j), cat=LpBinary) for j in r]
      for i in r]  # kw_i から kw_j に繋げるかどうか (1)
yb = [LpVariable('y%d' % i, lowBound=0) for i in r]  # kw_iが先頭かどうか (2)
zb = [LpVariable('z%d' % i, lowBound=0) for i in r]  # kw_iの順番 (3)
m += lpSum(xb[i][j] for i in r for j in r)  # なるべく繋げる (0)
for i in r:
    cou = lpSum(xb[i][j] for j in r)  # kw_i から出る数
    cin = lpSum(xb[j][i] for j in r)  # kw_i へ入る数
    m += cou <= 1  # kw_i から出る数は1以下 (4)
    m += cin <= 1  # kw_i へ入る数は1以下 (5)
    m += cou <= cin + yb[i]  # yに関する制約 (6)
    for j in r:
        m += zb[i] <= zb[j] - 1 + (n + 1) * (1 - xb[i][j])  # zに関する制約 (7)
m += lpSum(yb) == 1  # 先頭は1つだけ (8)
print('Pretreatment finished, now start solving...')
m.solve()  # 求解
print(int(value(m.objective)) + 1)  # 最長しりとり数
rr = range(1, n + 1)
vx = np.vectorize(value)(xb).astype(int)
i, s = 0, int(np.vectorize(value)(yb) @ rr)

with open('longest_list.txt', 'w', encoding='UTF-8') as fo:
    fo.write(f'Longest list: {int(value(m.objective)) + 1} names in total.\n')
    while s:
        if i:
            print(' -> ', end='')
        i += 1
        print('[%d]%s' % (i, kw[s - 1]), end=' ')
        s = vx[s - 1] @ rr
        fo.write(f'{pokemons[s - 1]}\n')
