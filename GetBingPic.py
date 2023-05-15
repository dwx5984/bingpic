# -*- coding: utf-8 -*-
import configparser
import datetime
import getpass
import json
import os.path
import time
import urllib.request

NICE_BING_URL = 'https://bing.open.apith.cn/all?pageSize=10&pageNum='
user = getpass.getuser()
LOCAL_PATH = os.path.expanduser('~') + '/Pictures/BingPic'


def save_img(base_url, dirname):
    # 保存图片到磁盘文件夹dirname中
    try:
        if not os.path.exists(dirname):
            print('文件夹', dirname, '不存在，重新建立')
            # os.mkdir(dirname)
            os.makedirs(dirname)

        # 请求bing美图api
        page = 114
        while True:
            print('正在获取第' + str(page) + '页的图片！')
            url = base_url + str(page)
            response = urllib.request.urlopen(url)
            result = json.loads(response.read())
            # 获得图片文件名和图片链接
            pics = result.get('data').get('item')
            index = 1
            for data in pics:
                # nice bing 返回数据有差别，今日美图data为json， 随机美图数据为数组
                img_name = data.get('filename')
                img_url = 'https:' + data.get('url')
                # 拼接目录与文件名，得到图片路径
                filepath = os.path.join(dirname, img_name)
                # 下载图片，并保存到文件夹中
                if not os.path.exists(filepath):
                    urllib.request.urlretrieve(img_url, filepath)
                    print('已保存:' + filepath + '。   第' + str(index+(page*10)))
                    time.sleep(10)
                else:
                    print(filepath + '已存在')
                index += 1
            page += 1
            time.sleep(10)
    except IOError as exception:
        print('文件操作失败', exception)
    except Exception as exception:
        print('错误 ：', exception)

#
# # 获取现在到明天凌晨后5分钟的秒数
# def get_sec_to_tomorrow():
#     now = datetime.datetime.now()
#     now_str = now.strftime('%Y-%m-%d %H:%M:%S')
#     dt = datetime.datetime.strptime(now_str, '%Y-%m-%d %H:%M:%S')
#     tomorrow_str = (dt.date() + datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
#     tomorrow = datetime.datetime.strptime(tomorrow_str, '%Y-%m-%d %H:%M:%S')
#     return (tomorrow - now).seconds + 5 * 60


# def main(img_type, t=None):
#     if t:
#         # 每隔t分钟随机获取壁纸
#         while True:
#             save_img(NICE_BING_URL, img_type, LOCAL_PATH)
#             time.sleep(t * 60)
#     else:
#         save_img(NICE_BING_URL, img_type, LOCAL_PATH)  # 获取今日壁纸
#         # 现在到明天凌晨后5分钟挂起线程
#         time.sleep(get_sec_to_tomorrow())
#         # 如果用户还没有关闭电脑（或未关闭此程序）, 则每过一天执行获取图片换壁纸
#         while True:
#             save_img(NICE_BING_URL, img_type, LOCAL_PATH)
#             time.sleep(24 * 60 * 60)


# def get_config():
#     root_dir = os.path.dirname(os.path.abspath(__file__))
#     configs = configparser.ConfigParser()
#     c = configs.read(root_dir + "/config.conf", encoding='UTF-8')
#     print(c)
#     print(configs.sections())
#     print(len(configs.sections()))
#     if len(configs.sections()) > 0:
#         try:
#             run_type = configs.get('settings', 'type')
#             minute = configs.get('settings', 'minute')
#             return {'type': run_type, 'minute': minute}
#         except Exception as ea:
#             print('配置文件损坏')
#             return None
#     else:
#         print('未找到配置文件，默认获取今日美图')
#         return None


if __name__ == "__main__":
    save_img(NICE_BING_URL, LOCAL_PATH)
    # settings = get_config()
    # # 没有配置
    # if settings is None:
    #     main('today')
    # else:
    #     run_type = settings.get('type')
    #     # 配置不是random
    #     if run_type != 'random':
    #         main('today')
    #     else:
    #         mintue = settings.get('minute')
    #         # 没配置时间
    #         if mintue is None:
    #             main('today')
    #         else:
    #             m = 30
    #             try:
    #                 m = int(mintue)
    #                 # 数字小于1
    #                 if m < 1:
    #                     main('random', 30)
    #                 else:
    #                     main('random', m)
    #             # 转换数字失败，默认30分钟一换
    #             except ValueError as e:
    #                 main('random', m)
