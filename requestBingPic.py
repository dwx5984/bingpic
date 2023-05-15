# -*- coding: utf-8 -*-
import time
import urllib2

NICE_BING_URL = 'https://bing.open.apith.cn/'


def get_img():
    try:
        url = NICE_BING_URL + 'random'
        response = urllib2.Request(url)
    except Exception as exception:
        print('错误 ：', exception)


def main():
    while True:
        get_img()
        time.sleep(30 * 60)


if __name__ == "__main__":
    main()
