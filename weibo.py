# # coding:utf8
# # time:2019/3/2
# # author:1415140539
# # task:weibomsg

import urllib
from http import cookiejar
from selenium import webdriver
import time
import re
class weibo:
    def __init__(self,name,password):
        self.name = name
        self.password = password
        self.Browser = webdriver.Chrome()
        self.url = "https://passport.weibo.cn/signin/login?entry=mweibo&r=https%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt="
    def driver_browser_to_log(self):
        self.Browser.get(self.url)
        time.sleep(10)
        self.Browser.find_element_by_id('loginName').send_keys(self.name)
        self.Browser.find_element_by_id('loginPassword').send_keys(self.password)
        self.Browser.find_element_by_id('loginAction').click()
        time.sleep(10)
        self.Browser.get('https://weibo.cn/')
        self.find_people("yuanke")
    def find_people(self,name):
        time.sleep(2)
        self.Browser.find_element_by_name('keyword').send_keys(name)
        self.Browser.find_element_by_name('suser').click()
        self.get_msg(str(self.Browser.page_source))
    def get_msg(self,html):
        # pattern = '<td valign="top"><a href="[\s\S]+?">([\s\S]+)</a><img src="https://h5.sinaimg.cn/upload/2016/05/26/319/5547.gif" alt="达人"><img src="https://h5.sinaimg.cn/upload/2016/05/26/319/donate_btn_s.png" alt="M"><br>粉丝2339人&nbsp;北京<br><div><form action="/attention/add?uid=1936103685&amp;rl=1&amp;st=176523" method="post"><div><input type="submit" value="关注"></div></form></div></td>'
        pattern ='<td valign="top">[\s\S]+?>([\s\S]+?)<'
        people = '粉丝([\s\S]+?)<'
if __name__ == "__main__":
    # cookie = cookiejar.CookieJar()
    # handler = urllib.request.HTTPCookieProcessor(cookie)
    # opener = urllib.request.build_opener(handler)
    # opener.addheaders = [("user-agent",'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36')]
    w = weibo("15383436475","151096a")
    w.driver_browser_to_log()