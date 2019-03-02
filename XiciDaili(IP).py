# coding:utf-8
# task:爬取国内高匿代理IP
from multiprocessing import pool,Manager
import urllib
import re
import json
from bs4 import BeautifulSoup
import functools
import re
import time
#获取网页的html
def get_one_page(url):
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36'}
    req= urllib.request.Request(url,headers = headers)
    res = urllib.request.urlopen(req)
    html = res.read().decode()
    #将得到网页进行解码,传递给get_html_msg进行进一步分析
#对html进行分析(IP,PORT,ADDRESS,TYPE,SPEED,CONNECT_TIME,TIME,TIME_DEFINE)
    return html
def get_html_msg(html):
    soup = BeautifulSoup(html,"html.parser")
    #用Beautiful得到一大块数据，然后进行进一步的筛选
    tbody = soup.find("table")
    return str(tbody)

def deal_table(html):
    soup = BeautifulSoup(html,"html.parser")
    trs = soup.find_all('tr')
    return trs


def save_to_file(msg):
    with open('proxyip.txt','a',encoding="utf8") as f:
        # json格式
        f.write(json.dumps(msg,ensure_ascii=False)+"\n")


def get_msg(html):
    pattern = ">([\s\S]+?)<"
    #这里有个坑，仔细观察会发现 bar_inner fast  bar_inner low
    pattern_speed = '<div class="bar_inner [\w]+" style="width:([\s\S]+?)">'
    L = re.findall(pattern_speed,html)
    l = re.findall(pattern,html)
    for i in l:
        if i == '\n':
            continue
        L.append(i)
    # print(L)
    if len(L) == 10:
        dic =  {
            "IP":L[3],
            "PORT":L[4],
            "Address":L[5],
            "is_ni":L[6],
            "Type":L[7],
            "Exists_time":L[8],
            "Time_define":L[9],
            "Speed":L[0],
            "Connect_T":L[1]
        # IP, PORT, ADDRESS, TYPE, SPEED, CONNECT_TIME, TIME, TIME_DEFINE
    }
    else:
        #有两条没有 地址
        dic = {
            "IP": L[3],
            "PORT": L[4],
            "is_ni": L[5],
            "Type": L[6],
            "Exists_time": L[7],
            "Time_define": L[8],
            "Speed": L[0],
            "Connect_T": L[1]
        }
    yield dic
#对数据进行存储


def main(Lock,url,crawled,q):
    L,html = get_url(url)
    L1 = []
    for i in L :
        if i not in crawled:
            L1.append(i)
    q.put(L1)
    tbody =get_html_msg(html)
    trs = deal_table(tbody)
    for i in range(len(trs)):
        if i == 0:
            #第一个tr不用采取
            continue
        for item in get_msg(str(trs[i])):
            Lock.acquire()
            save_to_file(item)
            Lock.release()
    q.put(url)
#得到整个网页的页码标记
def get_url(url):
    html = get_one_page(url)
    L = []
    pattern = '<a href="([/n\d]+)">[\d]+</a>'
    for url in (re.findall(pattern,html)):
        L.append('https://www.xicidaili.com'+url)
    return  (L,html)
if __name__  == "__main__":
    # 采用进程池的方式进行爬取
    # 宽度优先进行爬取

    SLEEP = 2
    p = pool.Pool(4)
    manager = Manager()
    Lock = manager.Lock()
    queue = manager.Queue()
    my_main = functools.partial(main,Lock)
    url = 'https://www.xicidaili.com/nn/'
    itemUrls = get_url(url)
    crawled = []
    wait_crawl = []
    for item in itemUrls:
        if item not in crawled:
            wait_crawl.append(item)
        wait_crawl = list(set(wait_crawl))
    while wait_crawl:
        url = wait_crawl.pop(0) #从开头弹出一个url
        print("正在爬取"+url)
        p.apply_async(my_main,args=(url,crawled,queue))
        wait_crawl.extend(queue.get())
        wait_crawl = list(set(wait_crawl))
        time.sleep(5)
        crawled.append(queue.get())
    # p.apply_async(my_main(url))
    p.close()
    p.join()