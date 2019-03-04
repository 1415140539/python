import logging,sys
import time
import urllib,random

logger = logging.getLogger("testLogger1") #传递一个名字
# 定制一个Logger的输出格式
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
#创建日志:文件日志 终端日志
file_handler = logging.FileHandler("testLogger1.log")
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

# 设置默认日志级别
logger.setLevel(logging.DEBUG) #值只记录>=DEBUG 的级别

#吧文件日志和终端日志添加到日志处理器中
logger.addHandler(file_handler)
logger.addHandler(console_handler)

PROXY_RANGE_MAX = 10
PROXY_RANGE_MIN = 1
def downHtml(url,headers = [],
            proxy = {},
             timeout = 10 ,
             decodeInfo = "utf-8",
            num_retries = 10):
    """
    爬虫的get请求，考虑了UA等 http request head 部分设置
    支持代理服务器配置
    返回的状态码不是200，怎么处理
    超时问题，及网页的编码格式

    :param url:
    :param headers:
    :param proxy:
    :param num_retries:
    :return:
    一般来说 使用UA池和代理服务器池相结合的方式来某个页面，
    更加不容易被反爬
    动态的调整服务器的使用策略
    """
    html = None
    if num_retries <= 0:
        return html
    #调整动态服务器
    if random.randint(PROXY_RANGE_MIN,PROXY_RANGE_MAX) >= PROXY_RANGE:
        logger.info("No Proxy")
        proxy = None
    proxy_handler = urllib.request.ProxyHandler(proxy)
    opener = urllib.request.build_opener(proxy_handler)
    opener.addheaders = headers
    urllib.request.install_opener(opener)
    try:
        response = urllib.request.urlopen(url)
        html = response.read().decode(decodeInfo)
        return html
    except UnicodeDecodeError:
        logger.error("UnicodeDecodeError")
    except urllib.error.URLError or urllib.error.HttpError as e:
        logger.error("urllib error")
        if hasattr(e,"code") and 400<= e.code < 500:
            logger.error("Client error")  # 客户端问题,通过分析日志来追踪
        elif hasattr(e,"code") and 500 <= e.code < 600 :
            html = downHtml( url ,
                             headers,
                             proxy,
                             timeout,
                             decodeInfo,
                             num_retries-1)
            time.sleep(PROXY_RANGE) #休息的时间可以自己定义一个
    except:
        logger.error("Download error")
PROXY_RANGE = 2

if __name__ == "__main__":
    url = "https://www.douban.com/doulist/3516235/"
    headers = [("User-Agent",'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36')]
    proxy = {"http":"117.90.2.18:9999"}
    print(downHtml(url,headers,proxy))
    logger.removeHandler(file_handler)
    logger.removeHandler(console_handler)