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

