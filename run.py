import os
import re


# 文件和文件夹重命名函数
def re_name(file_name):
    pattern = re.compile('[a-zA-Z]{3,7}-?\d{2,5}')
    match = re.search(pattern, file_name)
    file_name_re = str(match.group())
    hyphen = re.compile('-')
    have_hyphen = re.search(hyphen, file_name_re)
    if have_hyphen is None:
        d = re.compile('\d+')
        d2 = re.search(d, file_name_re)
        return re.sub(d, '-' + str(d2.group()), file_name_re)
    else:
        return file_name_re


# obj_dir = os.getcwd()
obj_dir = "D:\迅雷下载\H_test"
# print(obj_dir)
obj_list = os.listdir(obj_dir)
# print(obj_list)
for x in obj_list:
    file = os.path.join(obj_dir, x)
    # 判断是否为文件
    if os.path.isfile(file):
        name, ext = os.path.splitext(x)
        if ext != '.torrent':
            print(file)
            print(re_name(x))
    else:
        print(file)
        print(re_name(x))
