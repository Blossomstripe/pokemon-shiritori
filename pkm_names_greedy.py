import copy


def last_katakana(rust_str):
    dict_alter = {'ァ': 'ア', 'ィ': 'イ', 'ゥ': 'ウ', 'ェ': 'エ', 'ォ': 'オ'}
    last_ka = rust_str[-1]
    if last_ka == '\u30fc':
        last_ka = rust_str[-2]
    if last_ka in dict_alter.keys():
        last_ka = dict_alter[last_ka]
    return last_ka


if __name__ != '__main__':
    exit()

# 读入名字列表
names = list()
with open(file='pkm_names.txt', mode='r', encoding='UTF-8') as fo:
    while True:
        line = fo.readline()
        if line:
            names.append(line[:-1])
        else:
            break

# 构建首假名字典
dict_katakana_ori = dict()
for tar_name in names:
    first_ka = tuple(tar_name)[0]
    if first_ka in dict_katakana_ori.keys():
        dict_katakana_ori[first_ka].append(tar_name)
    else:
        dict_katakana_ori[first_ka] = [tar_name]

# 贪心搜索
max_list_result = list()
'''目前最长接龙长度'''
max_len = 0
run_times = 0
for first_name in names:
    dict_katakana = copy.deepcopy(dict_katakana_ori)
    list_result = list()
    '''将可接名字加入result列表，并在字典中删除该名字'''
    list_result.append(first_name)
    curr_name = tuple(first_name)
    dict_katakana[curr_name[0]].remove(first_name)
    while True:
        # 将可接名字组成列表，若列表为空则break
        last_ka = last_katakana(curr_name)
        try:
            list_alt = dict_katakana[last_ka]
        except KeyError:
            break
        if list_alt.__len__() == 0:
            break
        # 寻找可接名字中继续可接名字最多的一个
        max_possi = 0
        curr_name = list_alt[0]
        for i in list_alt:
            rast_alt_name = tuple(i)
            alt_last_ka = last_katakana(rast_alt_name)
            try:
                possi = dict_katakana[alt_last_ka].__len__()
            except KeyError:
                possi = 0
            if possi > max_possi:
                max_possi = possi
                curr_name = i
        # 将可接名字加入result列表，并在字典中删除该名字
        list_result.append(curr_name)
        temp = curr_name
        curr_name = tuple(curr_name)
        dict_katakana[curr_name[0]].remove(temp)
        del temp
    # 若目前接龙长度比目前最长的更长，则复制一份
    if list_result.__len__() > max_len:
        max_list_result = list_result[:]
        max_len = list_result.__len__()
    run_times += 1
    print(run_times)

with open('longest_list_v1.1.txt', 'w', encoding='UTF-8') as fo:
    fo.write(f'Longest list: {max_list_result.__len__()} names in total.\n')
    for i in max_list_result:
        fo.write(f'{i}\n')
print(max_list_result)
