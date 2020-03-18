import re
from bs4 import BeautifulSoup
import requests
import random
import time
import json
import pymysql
import pandas as pd
import html
import csv
import pymongo
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

headers_nocookie = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
    'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
}

cookies = {
    "CURRENT_FNVAL": "16",
    "_uuid": "A44FDE55-496C-908C-481F-985FD001019907627infoc",
    "buvid3": "6327CADC-50E0-4418-8AFD-FC889EE49D79155823infoc",
    "LIVE_BUVID": "AUTO5615838360099805",
    "rpdid": "|(k|k)m~RR~Y0J'ul)J)JY|u|",
    "CURRENT_QUALITY": "80",
    "INTVER": "1",
    "sid": "7wuvrlef",
    "DedeUserID": "327973223",
    "DedeUserID__ckMd5": "bcb4520ee29c8085",
    "SESSDATA": "2b276f03%2C1599878752%2Cf33af*31",
    "bili_jct": "74a605aedd7eb37ea6249ae8c85ea703",
    "PVID": "11"
}

headers = {
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
    'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6',
    # 'Cookie': 'CURRENT_FNVAL=16; _uuid=A44FDE55-496C-908C-481F-985FD001019907627infoc; buvid3=6327CADC-50E0-4418-8AFD-FC889EE49D79155823infoc; LIVE_BUVID=AUTO5615838360099805; rpdid=|(k|k)m~RR~Y0J\'ul)J)JY|u|; CURRENT_QUALITY=80; INTVER=1; sid=7wuvrlef; DedeUserID=327973223; DedeUserID__ckMd5=bcb4520ee29c8085; SESSDATA=2b276f03%2C1599878752%2Cf33af*31; bili_jct=74a605aedd7eb37ea6249ae8c85ea703; PVID=9'
}


def current_time():
    '''
    返回当前时间
    :return:
    '''
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def notice_wechat(title, content):
    '''server酱通知微信'''
    api = "https://sc.ftqq.com/SCU34444T94b6628ac7cdafb625a54ed4d75976545e6f70180d158.send"
    data = {
        'text': title,
        'desp': content
    }
    req = requests.post(api, data)


def get_outer_urls(keyword, page):
    '''【分页网址url采集】
     n：爬取页数
     结果：得到分页网页的list
     '''
    urllst = []
    for i in range(page):
        ui = f'https://search.bilibili.com/all?keyword={keyword}&page={i + 1}'
        urllst.append(ui)
    return urllst


def get_inter_urls(ui):
    '''
    【视频页面av号采集】
    ui：视频信息网页url
    结果：得到一个视频页面的list
    '''
    ri = requests.get(ui, headers)
    soupi = BeautifulSoup(ri.text, 'html.parser')
    lis = soupi.find('ul', {'class': 'video-list clearfix'}).find_all('li')
    lst = []
    for li in lis:
        lst.append(re.search('av\d+', li.a['href']).group(0))
    return lst


def get_danMuKu(cid):
    '''
    ui：视频页面网址
    table：mongo集合对象
    '''
    # ri = requests.get(ui, headers)
    # soupi = BeautifulSoup(ri.text, 'html.parser')
    # # title = soupi.find(id = "viewbox_report").span.text
    # title = soupi.h1['title']  # 标题
    # upload_time = soupi.find("span", {'class': 'a-crumbs'}).next_sibling.text  # 上传时间
    # # upload_time = re.search(r'(20.*\d)',soupi.find("div",class_ ="video-data").text)
    # play_count = soupi.find("div", {'class': 'video-data'})  # 播放量

    # 弹幕
    # cid = re.search(r'"cid":(\d*),', ri.text).group(1)  # cid

    cid_url = f"https://comment.bilibili.com/{cid}.xml"
    try:

        danmaku_request = requests.get(cid_url, headers=headers)
        html = danmaku_request.content
        html_doc = str(html, 'utf-8')
        danmuku_soup = BeautifulSoup(html_doc, "html.parser")
        results = danmuku_soup.find_all('d')
        i = 0
        j = 10
        if (len(results) < 10):
            j = len(results)

        print("弹幕个数为： {}".format(len(results)))

        # 拼接弹幕
        a = ''
        while (i < j):
            a = a + results[i].text + "---"
            i += 1

        return a
    except Exception as e:
        print(e)
        notice_wechat("弹幕爬取失败", len(results))

    # dmlst = re.findall(r'<d.*?/d>', r2.text)
    #
    # dm=dmlst[0]
    # print(title)
    # print(upload_time)
    # print(cid)
    # print(re.search(r'>(.*)<', dm).group(1))
    # print(re.search(r'p="(.*)">', dm).group(1))
    # for dm in dmlst:
    #     dic = {}
    #     dic['标题'] = title
    #     dic['上传时间'] = upload_time
    #     dic['cid'] = cid
    #     dic['弹幕内容'] = re.search(r'>(.*)<', dm).group(1)
    #     dic['其他信息'] = re.search(r'p="(.*)">', dm).group(1)
    #     # table.insert_one(dic)
    #     n += 1


url = 'https://api.bilibili.com/x/web-interface/view?aid={}'
k = 0


def get_video_detail(id,flag):
    '''

    :param id: av号
    :param flag: 标志为，1为包含'av',0为纯数字
    :return:
    '''
    global k
    k = k + 1
    print("记录编号： {}".format(k))
    full_url = url.format(id[2:])
    try:
        res = requests.get(full_url, headers=headers, cookies=cookies, timeout=30)
        time.sleep(random.random() + 1)
        print('正在爬取{}'.format(id))
        content = json.loads(res.text, encoding='utf-8')
        # test = content['data']

    except:
        print('error')
        info = {'视频id': id, '最新弹幕数量': '', '金币数量': '', '不喜欢': '', '收藏': '', '最高排名': '', '点赞数': '', '目前排名': '', '回复数': '',
                '分享数': '', '观看数': ''}
        return info
    else:

        cid = content['data']['cid']
        title = content['data']['title']
        danmuku = get_danMuKu(cid)

        desp = content['data']["desc"].replace('\n', "--").replace(' ', '')
        danmu = content['data']['stat']['danmaku']
        coin = content['data']['stat']['coin']
        dislike = content['data']['stat']['dislike']
        favorite = content['data']['stat']['favorite']
        his_rank = content['data']['stat']['his_rank']
        like = content['data']['stat']['like']
        now_rank = content['data']['stat']['now_rank']
        reply = content['data']['stat']['reply']
        share = content['data']['stat']['share']
        view = content['data']['stat']['view']

    info = {'视频id': id, '标题': title, '描述': desp, '最新弹幕数量': danmu, '金币数量': coin, '不喜欢': dislike, '收藏': favorite,
            '最高排名': his_rank, '点赞数': like,
            '目前排名': now_rank, '回复数': reply, '分享数': share, '观看数': view, '弹幕内容': danmuku}

    return info


# 连接数据库
try:
    con = pymysql.connect(
        host="localhost",
        port=3306,
        user='root',
        password='qwe123456',
        database='bsite'
    )
except:
    notice_wechat("数据库连接失败啦", "时间为： " + current_time())


def insert_mysql(data):
    '''
    插入mysql数据库
    :param data:
    :return:.
    '''
    sql = "insert into video(id,title,desp,danmu,coin,dislike,favorite,his_rank,like_count,now_rank,reply,share,view,danmuku) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    # sql = "insert into video(id,title,desp) values(%s,%s,%s);"
    # val = ('测试1', '测试内容1')
    values_list = data.values()
    values = tuple(values_list)
    # values = values[0:3]
    print(values)
    # values=("av85314885","我是题目","我想这大概是过得最无聊的春节了吧，突如来的病毒让我们只能留在家中--原本我计划的休息也变成了肝视频--恨死了这该死的病毒了--希望大家保护好自己--出门记得戴口罩，尽量不去避免人员密集地方--拒绝野味~！！--武汉加油，中国加油------借物表：--模型：战双帕弥什-露西亚/Pocket-Vocaloid/Lct红枣/椛暗/军士--动作：绅士黑衣--镜头：绅士黑衣--场景：胧月兔--MME：Burner/thunter/Rui_斯基/Ikeno--原片地址：搬运：av3290381--https://www.youtube.com/watch?v=Z8piSgx_CUM搬运自https://www.youtube.com/watch?v=Z8piSgx_CUM")
    # values[2]="eqeqweqw"

    # print(len("【战双帕弥什】帕弥什病毒vs新型冠状病毒"))
    cursor = con.cursor()
    try:
        cursor.execute(sql, values)
        con.commit()
        print("插入成功")
    except Exception as e:
        con.rollback()
        # print(type(e))
        # ss=str(e)
        # print(ss)
        notice_wechat("插入数据库失败", "时间: " + current_time() + ", av号： " + data['视频id'] + ", 异常信息： " + str(e))
        print("插入失败")
        print(e)


def toCSV(data, flags):
    '''
    将抓取到的数据转换成CSV文件
    :param data:数据
    :param flags:标志位 0：元组，1：字典
    :return:
    '''
    # write_clo = ['第一列', '第二列', '第三列', '第四列']
    if flags == 1:
        write_clo = data.values()
    else:
        write_clo = data
    try:
        df = pd.DataFrame(columns=(write_clo))
        df.to_csv("bilibili.csv", line_terminator="\n", index=False, mode='a', encoding='utf8')
    except Exception as e:
        notice_wechat("csv导入异常", "时间: " + current_time() + ", av号： " + data['视频id'], ", 异常信息： " + str(e))
        print(e)

    # python2可以用file替代open
    # with open("bilibili.csv", "w") as csvfile:
    #     writer = csv.writer(csvfile)
    #
    #     # 先写入columns_name
    #     writer.writerow(['第一列','第二列','第三列','第四列'])
    #     # 写入多行用writerows
    #     writer.writerows([[0, 1, 3], [1, 2, 3], [2, 3, 4]])


# def send_email(filelist, content=""):
#     '''
#     完成后发送文件到邮箱
#     :param data:
#     :return:
#     '''
#     smtpHost = 'smtp.139.com'  # 139邮箱SMTP服务器
#     sendAddr = '发送人邮箱'
#     password = '邮箱密码'  # 163邮箱,则为授权码
#     receiver = '收件人邮箱'
#     subject = "邮件标题"
#     content = '正文内容'
#
#     msg = MIMEMultipart()
#     msg['from'] = sendAddr
#     msg['to'] = receiver
#     msg['Subject'] = subject
#
#     txt = MIMEText(content, 'plain', 'utf-8')
#     msg.attach(txt)  # 添加邮件正文
#
#     # 添加附件,传送filelist列表里的文件
#     filename = ""
#     i = 0
#     for file in filelist:
#         i = i + 1
#         filename = file
#         # print(str(i),filename)
#         part = MIMEApplication(open(filename, 'rb').read())
#         part.add_header('Content-Disposition', 'attachment', filename=filename)
#         msg.attach(part)
#
#     server = smtplib.SMTP(smtpHost, 25)  # SMTP协议默认端口为25
#     # server.set_debuglevel(1)  # 出错时可以查看
#
#     server.login(sendAddr, password)
#     server.sendmail(sendAddr, receiver, str(msg))
#     print("\n" + str(len(filelist)) + "个文件发送成功")
#     server.quit()

def insert_mongo(data):
    '''
    插入mongodb数据库
    :param data:
    :return:
    '''
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    db = myclient['blibli']
    database = db['data']

    database.insert_one(data)


def sentTest():
    host = 'smtp.163.com'
    # 设置发件服务器地址
    port = 465
    # 设置发件服务器端口号。注意，这里有SSL和非SSL两种形式，现在一般是SSL方式
    sender = 'goddong12580@163.com'
    # 设置发件邮箱，一定要自己注册的邮箱
    pwd = 'LROTXBPDZSYYDEJK'
    # 设置发件邮箱的授权码密码，根据163邮箱提示，登录第三方邮件客户端需要授权码
    receiver = '923219711@qq.com'
    # 设置邮件接收人，可以是QQ邮箱
    body = '<h1>抓取完成</h1><p>请查看附件</p>'
    # 设置邮件正文，这里是支持HTML的
    msg = MIMEText(body, 'html')
    # 设置正文为符合邮件格式的HTML内容
    msg['subject'] = '打卡通知'
    # 设置邮件标题
    msg['from'] = sender
    # 设置发送人
    msg['to'] = receiver
    # 设置接收人
    try:
        s = smtplib.SMTP_SSL(host, port)
        # 注意！如果是使用SSL端口，这里就要改为SMTP_SSL
        s.login(sender, pwd)
        # 登陆邮箱
        s.sendmail(sender, receiver, msg.as_string())
        # 发送邮件！
        print('发送邮件成功')
    except smtplib.SMTPException:
        print(current_time() + '发送邮件失败！！')


def sendMail(title, att_name):
    '''
    :param title: 邮件标题
    :param att_name: 附件名，生成的csv附件名
    :return:
    '''
    sender = 'goddong12580@163.com'
    pwd = 'DVCDOGAJMNFJMRAC'
    receivers = '923219711@qq.com'  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    # 创建一个带附件的实例
    try:
        message = MIMEMultipart()
        message['From'] = Header("傻有钱企业", 'utf-8')
        message['To'] = receivers
        subject = title
        message['Subject'] = Header(subject, 'utf-8')

        # 邮件正文内容
        message.attach(MIMEText('爬虫抓取完成数据抓取完成请下载附件', 'plain', 'utf-8'))

        # 构造附件1，传送当前目录下的 test.txt 文件
        att1 = MIMEText(open(att_name, 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        att1["Content-Disposition"] = 'attachment; filename="{}"'.format(att_name)
        message.attach(att1)
    except Exception as e:
        print(e)

    # 构造附件2，传送当前目录下的 runoob.txt 文件
    # att2 = MIMEText(open('runoob.txt', 'rb').read(), 'base64', 'utf-8')
    # att2["Content-Type"] = 'application/octet-stream'
    # att2["Content-Disposition"] = 'attachment; filename="runoob.txt"'
    # message.attach(att2)

    try:
        smtpObj = smtplib.SMTP_SSL('smtp.163.com', 465)
        smtpObj.login(sender, pwd)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print
        "邮件发送成功"
    except smtplib.SMTPException:
        print
        "Error: 无法发送邮件"


def inner_urlBy_api(page, keyword):
    '''
    通过api抓取av号
    :param keyword: 关键字
    :param page: 页数
    '''
    lis = []
    for i in range(page):

        time.sleep(random.random()+1)
        search_api = "https://api.bilibili.com/x/web-interface/search/all/v2?page={}&order=&keyword={}".format(i + 1,keyword)
        # search_api = "https://api.bilibili.com/x/web-interface/search/all/v2?page={}&order=&keyword={}".format(1,keyword)

        res=requests.get(search_api,headers=headers,timeout=30)
        html_json=json.loads(res.text,encoding='utf-8')
        data=html_json['data']['result'][8]['data']
        for item in data:
            lis.append(item['aid'])
            # print(item['aid'])

    # print(lis)
    return lis

    # if(len(data['data'])<=0):
    #     print("为空")
    # else:
    #     print("不为空")
    # lis.append(search_api)

    # return lis
    # print(lis)


if __name__ == '__main__':
    # print(get_video_detail("av89309972",1))

    # get_danMuKu(152771439)
    # url = "https://www.bilibili.com/video/av85859671?from=search&seid=10530534315860999666"
    # print(re.search('av\d+', url).group(0))

    # '视频id': id, '标题': title, '描述': desp, '最新弹幕数量': danmu, '金币数量': coin, '不喜欢': dislike, '收藏': favorite,
    # '最高排名': his_rank, '点赞数': like,
    # '目前排名': now_rank, '回复数': reply, '分享数': share, '观看数': view, '弹幕内容': danmuku

    # top = ['视频id', '标题', '描述', '最新弹幕数量', '金币数量', '不喜欢', '收藏', '最高排名', '点赞数', '目前排名', '回复数', '分享数', '观看数', '弹幕内容']
    # toCSV(top, 0)
    # outer_url=get_outer_urls("冠状病毒",50)
    # for item in outer_url:
    #     inner_url = get_inter_urls(item)
    #     time.sleep(0.5)
    #     for p in inner_url:
    #         data = get_video_detail(p,1)
    #         insert_mysql(data)
    #         toCSV(data, 1)
    # data = get_video_detail("av85314885",1)
    # insert_mysql(data)

    inner_urlBy_api(10, "冠状病毒")

    # print(current_time())

    # url = 'https://search.bilibili.com/all?keyword=冠状病毒'
    # urllst = get_outer_urls(20)  # 获取前20页的网址
    # u1 = urllst[0]  # 获取第一页的全部20个视频url
    # url_inter = get_inter_urls(u1)  # 获取第一个视频的url
    #
    # myclient = myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    # db = myclient['blibli']
    # datatable = db['data']
    #
    # # get_data(url_inter[0],dic_headers,dic_cookies,datatable)
    #
    # errorlst = []
    # count = 0
    # for u in url_inter:
    #     try:
    #         count += get_data(u, headers)
    #         print('数据采集并存入成功，总共采集{}条数据'.format(count))
    #     except:
    #         errorlst.append(u)
    #         print('数据采集失败，数据网址为：', u)
    #         notice_wechat("数据采集失败","数据采集失败，数据网址为: "+u)

    # url = "https://www.bilibili.com/video/av69241910?p=1"
    # req = requests.get(url, headers)
    # soup = BeautifulSoup(req.text, "html.parser")
    # print(soup.find("span", {'class': 'dm'})['title'])
    # print(soup.h1['title'])

    con.close()
    # sendMail("数据抓取完成","bilibili.csv")
    # notice_wechat("抓取成功啦", current_time()+"请查看数据库")
