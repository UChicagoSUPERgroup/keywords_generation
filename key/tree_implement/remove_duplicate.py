
def remove_duplicate(ls_ls):
    remove_dic = {}

    for ls in ls_ls:
        for word in ls:

            if word in remove_dic.keys():
                remove_dic[word] += 1
            else:
                remove_dic[word] = 1
    rm_ls = [word for word in remove_dic.keys() if remove_dic[word] > 1]
    new_ls = []
    for ls in ls_ls:
        ls = [word for word in ls if word not in rm_ls]
        new_ls.append(ls)

    return new_ls


def intersect(ls_ls):
    if len(ls_ls) < 2:
        return ls_ls

    inter = set(ls_ls[0])

    for ls in ls_ls:
        inter = inter & set(ls)

    return inter


def remove_duplicate_2(ls_ls):
    inter = intersect(ls_ls)
    for i in range(0, len(ls_ls)):
        ls_ls[i] = [ele for ele in ls_ls[i] if ele not in inter]

    return ls_ls
