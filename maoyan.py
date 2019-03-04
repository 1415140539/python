
import random
import re
import json
import time
import requests
from multiprocessing import Pool, Manager
import functools
from douban import mypymysql





# 万能的正则([\s\S]*?)
# 使用关键确定好开始和结束
#http://maoyan.com/board/4?offest=0
MAXSLEEPTIME = 3
MINSLEEPTIME = 2
STATU_OK = 200
MAX_PAGE_NUM = 10
SERVER_ERROR_MIN = 500
SERVER_ERROR_MAX = 600
CLIENT_ERROR_MIN = 400
CLIENT_ERROR_MAX = 500
NOTFOUNDERROR = 404
HAVENOTRIGHT = 403
#对于URL 如果发现规律的话， 优先考虑 使用规律。
# 如果实在发现不了规律 把url提取出来，要做去重的处理
# 抓取网页信息时：
# 需要设置UA，需要考虑出错时的处理，状态码5xx，4xx的处理:
# 5XX(怎么使用递归反复尝试，间隔时间需要一定的策略)
# 4XX(需要日志)
# 提取信息可能需要进一步的去重
# 写json 时需要注意，写进去的item是一种字典的形式；所以在提取时，可以使用字典的形式，以便将来做数据分析
# 1)对URL发起请求http request,得到相应的相应request response相应 我们所需的数据就在response的响应体里。
def get_one_page(URL, num_retries = 5):
    if num_retries == 0:
        return None
    ua_headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}
    response = requests.get(URL,headers = ua_headers)
    if response.status_code == STATU_OK : #OK
        return response.text
    elif  SERVER_ERROR_MIN<response.status_code<SERVER_ERROR_MAX:
        time.sleep(MINSLEEPTIME)
        get_one_page(URL,num_retries-1)
    elif  CLIENT_ERROR_MIN<=response.status_code<CLIENT_ERROR_MAX:
        if response.status_code == NOTFOUNDERROR:
            print("Page not Found")
        elif response.status_code ==HAVENOTRIGHT:
            print("Have no rights")
        else:
            pass
    return  None
# 2)使用正则表达式，XPath，Bs4精确的数据
def parse_one_page(html):
    pattern = re.compile('<p class="name">[\s\S]*?title="([\s\S]*?)"[\s\S]*?<p class="star">([\s\S]*?)</p>[\s\S]*?<p class="releasetime">([\s\S]*?)</p>')
    items = re.findall(pattern,html)
    for it in items:
        yield dict(file_name=it[0].strip(),
              star =it[1].strip(),
              time = it[2].strip()
                   )
# 3)存到本地的文件数据库中
def write_to_file(item):
    with open("猫眼.txt",'a',encoding = "utf-8") as f:
        f.write(json.dumps(item,ensure_ascii=False)+"\n")
#控制爬取一页的流程
def crawl_one_page(lock, offset):
    #拼出一个url
    url ="https://maoyan.com/board/4?offset="+str(offset)
    #下载这个url
    html = get_one_page(url)
    #解析每个页面并且把获取到的item写入文件
    for item in parse_one_page(html):
        lock.acquire()
        # write_to_file(item)
        write_to_sql(item)
        lock.release()
def write_to_sql(item):
    conn = mypymysql.my_py(db = "maoyan")
    sql = "insert into maoyan(file_name,start,time) values(%s , %s ,%s)"
    params = (item['file_name'],item["start"],item["time"])
    result = conn.execute(sql,params)
    if result:
        print("插入成功")
        return True
    else:
        print("插入失败")
        return False

time.sleep(random.randint(MINSLEEPTIME,MAXSLEEPTIME)) #随机休息1-3秒之后再进行下一次爬寻
if __name__ == "__main__":
    # for i in range(MAX_PAGE_NUM):
    #     crawl_one_page(i*10)
    # 在进程之间传递lock需要使用Manager的Lock
    manager = Manager()
    lock = manager.Lock()
    partial_Crawl = functools.partial(crawl_one_page, lock)
    pool = Pool(2)
    # 异步 pool.apply_async()
    # 使用偏函数对原来的函数进行一层包装
    pool.map(partial_Crawl,[i*10 for i in range(10)])
    pool.close() #不要再往里添加任务
    pool.join()
    # apply 同步
    # map (func,iterable)



# GIL:在python 当中一次只能有一个线程在跑 全局解释锁
# 在单核的年代是有好处的,让数据更加安全
# 在多核年代就成为了CPU使用的瓶颈。
# 在计算密集型场景，适合使用python多进程
# 高精密的计算，图形图像，神经网络计算
# 在IO密集型场景，适合使用python 的多线程及协程
# 比如爬虫程序就是一个典型的IO密集型操作
# 双核两个线程运行死循环 CPU 50%
# 双核两个进程运行死循环 CPU 100%
