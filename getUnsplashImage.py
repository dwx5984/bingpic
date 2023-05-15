# -*- coding: utf-8 -*-
import os.path
import time
import urllib.request
import pymysql


# 连接数据库
def crate_db():
    conn = pymysql.connect(host='localhost',
                           port=3306,
                           user='root',
                           password='root',
                           db='unsplash',
                           charset='utf8')
    return conn


def get_results(current, size):
    conn = crate_db()
    cur = conn.cursor()
    sql = "select * from `unsplash_pic` where category='4k/desktop' limit %s,%s" % (current, size)
    cur.execute(sql)
    results = cur.fetchall()
    return results


def save_to_path(dir_name, current, size):
    results = get_results(current - 1, size + 1)
    print(results)
    try:
        if not os.path.exists(dir_name):
            print('文件夹', dir_name, '不存在，重新建立')
            os.makedirs(dir_name)
    except IOError as exception:
        print('文件夹创建失败', exception)
    for item in results:
        link = item[1]
        imgId = item[3]
        filename = imgId + '.jpg'
        filepath = os.path.join(dir_name, filename)
        if not os.path.exists(filepath):
            print('保存文件到', filepath)
            urllib.request.urlretrieve(link, filepath)
            # 太频繁可能会被认为是攻击，这里休眠15秒
            waitSec = 10
            print('等待', waitSec, '秒')
            time.sleep(waitSec)
        else:
            print('文件已存在')


if __name__ == "__main__":
    # 这里保存到 C:\Users\{你的用户名}\Pictures\unsplash, 自行更改
    dirname = os.path.expanduser('~') + '/Pictures/unsplash/4k_desktop/'
    save_to_path(dirname, current=99, size=100 - 99)
