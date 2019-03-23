from lxml import etree
import requests
from bs4 import BeautifulSoup
import re
from rpcapi import *
import upyun
import time
import html2text
from jieba.analyse import *
from weiyuanchuang import *


up = upyun.UpYun('xxxx', 'xxxxxx', 'xxxxxx', timeout=30, endpoint=upyun.ED_AUTO)
UserName = 'xxxxxx'
PassWord = 'xxxxxxxxxx'
time = ''
title = ''
content = ''
urls = [
    'https://www.XXX.com/code/list_1.html',
    'https://www.XXX.com/code/list_2.html',
    'https://www.XXX.com/code/list_3.html',
    'https://www.XXX.com/code/list_4.html',
    'https://www.XXX.com/code/list_5.html',
    'https://www.XXX.com/code/list_6.html'
    ]

#获取二级目录
def get_url(urls:list):
    list = []
    for temp_url in urls:
        r = requests.get(temp_url)
        r.encoding = "utf-8"

        selector = etree.HTML(r.text)
        links = selector.xpath('//*[@id="list"]/li/a/@href')
        for link in links:
            list.append(link)
    return list

#改变图片链接&上传图片
def img_path(html):
    res = html
    p = re.compile(r'img src="//(?P<url>.*?)/(?P<path>.*?)"')
    headers = { 'x-gmkerl-thumb': '/quality/70' }
    for m in p.finditer(html):
        # print (m.groupdict())
        # print (m.group())
        f = requests.get('http://' + m.groupdict()['url'] + '/' + m.groupdict()['path'] ).content
        up.put('typecho/' + m.groupdict()['path'], f, checksum=False, headers=headers)
        res = p.sub('img src="https://你的又拍云域名/' + m.groupdict()['path'] + '"' , html)

    return res

#解析内容
def get_table(url:str):
    global time,content,title
    r = requests.get(url)
    r.encoding = "utf-8"
    pattern = re.compile(' <script src.*?javascript"></script>(.*?)<p>XXX网文章.*?</p>',re.S)
    items = re.findall(pattern,r.text)
    if len(items) == 0:
        return False
    temp_content = items[0].strip()
    content = to_markdown(img_path(temp_content))

    pattern = re.compile(' <h1 class.*?title">(.*?)</h1>',re.S)
    items = re.findall(pattern,r.text)
    if len(items) == 0:
        return False
    title = items[0].strip()

    pattern = re.compile('修订日期：(.*?) - (.*?)  发布自',re.S)
    items = re.findall(pattern,r.text)

    if len(items) != 1:
        return False
    temp_time = items[0][0] + ' ' + items[0][1]
    time = temp_time.replace('年', '-').replace('月', '-').replace('日', '').replace('时', ':').replace('分', ':').replace('秒', '')
    return True


#转换为Markdown格式
def to_markdown(html):
    h=html2text.HTML2Text()
    h.ignore_links=False
    return h.handle(html)

#记录进度
def jindu(url, status):
    x = 0
    if status == 'w':
        f = open('jindu.txt', 'a+')
        f.write(url+ '\n')
        x = 2
    if status == 'r':
        f = open('jindu.txt', 'r')

        for line in f:
            if line == url+'\n':
                x = 1
                break
    f.close()
    return x

#提取关键词
def keyword(html):
    temp_list = textrank(html, topK=2 , withWeight=False)
    if len(temp_list) != 2:
        temp_list = ['','']
    return temp_list

if __name__ == '__main__':
    xtitle = ''
    mw = MetaWeblog(UserName, PassWord)
    temp_list = get_url(urls)

    for temp_url in temp_list:
        if jindu(temp_url, 'r') == 1: 
            print ('已经发布：'+ temp_url)
            continue
        xtitle = ''

        if get_table(temp_url):
            for x in title:
                xtitle += x 
            xtitle = getSeoContent(xtitle, 80)
            content = getSeoContent(content, 80)

            if xtitle == 'ERR' or content == 'ERR':
                print ("ERR---->"+ temp_url)
                continue
            postid = mw.newPost(xtitle, '<!--markdown-->' + content, keyword(content)[0]+','+keyword(content)[1], 'Python', time)
            print (postid+ '--->'+ xtitle + '--->'+ time)
            jindu(temp_url, 'w')


