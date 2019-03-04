import basicSpider
from bs4 import BeautifulSoup
import re
'''
去重有两个部分第一次发生在已经爬取的队列中，第二次发生在已爬队列中
一个是已经爬取的队列,只进不出的，是历史记录
一个是带爬队列，有进有出,一旦这个带爬队列中没有元素可以
出了，说明当前的爬虫任务已经完成了
'''
def get_html(url,cred = [], cra=[]):
    '''
    得到网页信息
    :param url:
    :return:
    '''
    headers = [("User-Agent",
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36')]
    proxy = {"http":"117.90.2.18:9999"}
    html = basicSpider.downHtml(url,headers = headers,proxy=proxy)
    pattern = re.compile('(https://www.douban.com/doulist/3516235/\?start=.*?)"')
    itemUrls = re.findall(pattern, html)
    for item in itemUrls:
        if item not in cred:
            #第一步的去重,确定这些url不在已爬队列当中
            cra.append(item)
        #第二步区中,对带爬队列中去重
        cra = list(set(cred))
    return html
def get_move_detail(html):
    soup = BeautifulSoup(html,"html.parser")
    move_list = soup.find_all("div",class_="bd doulist-subject")
    for move in move_list:
        save_file(get_move_one(move))
def get_move_one(move):
    '''
    将得到的网页信息进行筛选
    :param move:
    :return:
    '''
    result = ""
    soup = BeautifulSoup(str(move),"html.parser")
    title = soup.find_all('div',class_="title")
    soup_title = BeautifulSoup(str(title[0]),"html.parser")
    for item in soup_title.stripped_strings:
        result += item
    try:
        score = soup.find_all("span",class_="rating_nums")
        score_ = BeautifulSoup(str(score[0]),"html.parser")
        for line in score_.stripped_strings:
            result +="||评分:"
            result += line
    except:
        result += "||评分:5.0"
    abstract = soup.find_all("div",class_ = "abstract")
    abstract_ = BeautifulSoup(str(abstract[0]),"html.parser")
    for item in abstract_.stripped_strings:
        result += "||"
        result += item
    result += "\n"
    return result
def save_file(move):
    '''
    将电影筛选出来的信息写入文件
    '''
    with open("move.txt","a",encoding="utf-8") as f:
        f.write(move)
if __name__ == "__main__":
    url = "https://www.douban.com/doulist/3516235/"
    html = get_html(url)
    pattern = re.compile('(https://www.douban.com/doulist/3516235/\?start=.*?)"')
    get_move_detail(html)
    itemUrls = re.findall(pattern,html)
    crawl_queue = []  #带爬队列
    crawled_queue = []  # 已经爬取的队列
    # 两步去重
    # 关系型数据库通过吧URL(做hash sha256，md5)设置为主键来去重
    for item in itemUrls:
        if item not in crawled_queue:
            #第一步的去重,确定这些url不在已爬队列当中
            crawl_queue.append(item)
        #第二步区中,对带爬队列中去重
        crawl_queue = list(set(crawl_queue))
    # 模拟广度优先遍历
    while crawl_queue: #去待爬队列中去值，知道带爬队列为空
        url = crawl_queue.pop(0)
        html = get_html(url,crawled_queue,crawl_queue)
        get_move_detail(html)
        crawled_queue.append(url)