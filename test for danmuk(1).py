# 用来爬取视频信息的代码嘿嘿嘿
# 导入库
import requests
# 导入requests module
from lxml import etree
import re
from pprint import pprint
import json
import urllib.request
import random
import time
from openpyxl import Workbook
import xlsxwriter
import time
import datetime
import json
import openpyxl

def getcid(av_num):  # 输入av号输出cid
    url_vid = "https://www.bilibili.com/video/av{}/".format(av_num)
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    }
    response = requests.get(url_vid, header)
    res = response.content.decode()

    cid_num = re.findall(r"\"pages\"\:\[\{\"cid\":(.*?)\,", res, re.S)[0]
    return cid_num


def get_danmuk(av_num):
    cid = getcid(av_num)
    url_danmuk = "https://comment.bilibili.com/{}.xml".format(cid)
    print(url_danmuk)
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    }
    cid_url = f"https://comment.bilibili.com/{cid}.xml"
    r2 = requests.get(url_danmuk, header)
    r2.encoding = r2.apparent_encoding
    danmuku_all = re.findall(r'<d.*?/d>', r2.text)

    n = 0
    for item in danmuku_all:
        timestamp = re.search(r'p="(.*)">', item).group(1).split(",")[4]

        lcaltime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(timestamp)))
        content=re.search(r'>(.*)<', item).group(1)
        print(lcaltime +" "+content)



def get_danmuk_t(av_num):
    cid = getcid(av_num)
    url_danmuk = "https://comment.bilibili.com/{}.xml".format(cid)
    print(url_danmuk)
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    }
    # response = requests.get(url_danmuk, header)
    #
    # res = response.content.decode()
    #
    #
    # print("0"*100)
    # pprint(res)
    # print("0" * 100)
    # html = etree.HTML(res.encode())
    # print(html)
    #
    # danmuk = html.xpath("//d/text()")
    r2 = requests.get(url_danmuk, header)
    r2.encoding = r2.apparent_encoding
    d = re.findall(r'<d.*?/d>', r2.text)

    print(d)
    n = 0
    dic = {}
    # for d_item in d:
    #
    #     dic['标题'] = title
    #     dic['上传时间'] = upload_time
    #     dic['cid'] = cid
    #     dic['弹幕内容'] = re.search(r'>(.*)<', dm).group(1)
    #     dic['其他信息'] = re.search(r'p="(.*)">', dm).group(1)
    #     # table.insert_one(dic)
    #     print(dm)
    #     n += 1
    # return n

    # return danmuk


if __name__ == '__main__':
    av_num = 85314885
    get_danmuk(av_num)

    # get_danmuk(av_num)
    # danmuk = get_danmuk(av_num)

    # print(danmuk)
