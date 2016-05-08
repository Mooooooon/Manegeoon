import os
import re
import pycurl
from io import BytesIO


# 封装CURL操作
def get_web(url):
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.SSL_VERIFYPEER, 0)
    c.setopt(c.SSL_VERIFYHOST, 0)
    c.setopt(c.CONNECTTIMEOUT, 60)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    body = buffer.getvalue()
    return body.decode('utf-8')


# 文件和文件夹重命名函数
def get_av_number(file_name):
    file_name = file_name.replace("SIS001", "")
    pattern = re.compile('[a-zA-Z]{3,7}-?\d{2,5}')
    match = re.search(pattern, file_name)
    av_no = str(match.group())
    hyphen = re.compile('-')
    have_hyphen = re.search(hyphen, av_no)
    if have_hyphen is None:
        d = re.compile('\d+')
        d2 = re.search(d, av_no)
        return re.sub(d, '-' + str(d2.group()), av_no)
    else:
        return av_no


# 获取视频信息
def get_av_info(no):
    html = get_web("https://avmo.pw/cn/search/" + no)
    pattern = re.compile('https://avmo.pw/cn/movie/[a-zA-z0-9]{4}')
    match = re.search(pattern, html)
    url = str(match.group())
    html = get_web(url)
    pattern = re.compile('<h3>(.*)</h3>')
    match = re.search(pattern, html)
    file_name = str(match.group(1))
    pattern = re.compile('<span class="genre"><a href=".{10,50}">(.{1,10})</a></span>')
    match = re.findall(pattern, html)
    for i in match:
        file_name += ' ' + i
    print(file_name)


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
            get_av_info(get_av_number(x))
    else:
        print(file)
        get_av_info(get_av_number(x))
