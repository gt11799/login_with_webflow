#!/usr/bin/env python
# _*_coding=utf8 _*_
'''
Crawl the online_time of zhihu user,
Need the user name and password
store the data in the mysql
'''

import requests
import cookielib
import random
import time
from lxml import etree

class CsdnSpider(object):
    
    def __init__(self, login, password, article):
        self.login = login
        self.password = password
        self.url = 'https://passport.csdn.net/account/login'
        self.article = random.choice(article)
        self.article_url = 'http://blog.csdn.net/gt11799/article/details/' + self.article
        
        self.jar = cookielib.CookieJar()
        self.pwd = {
            'username':self.login,
            'password':self.password,
            #'loginRedirect':random.choice(self.article_url),
            '_eventId':'submit',
        }
        self.header = {
            'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0',
        }
        
    def login_csdn(self):
        self.request = requests.get(self.url, cookies=self.jar)
        print("Geted request...")
        self.parse = etree.HTML(self.request.text)
        self.webflow = self.parse.xpath('//input[@name="lt"]/@value')
        self.execution = self.parse.xpath('//input[@name="execution"]/@value')
        #print self.webflow[0], self.execution[0]
        self.pwd["lt"] = self.webflow[0]
        self.pwd["execution"] = self.execution[0]
        #print self.pwd
        
        self.request = requests.post(self.url, headers=self.header, cookies=self.request.cookies, data=self.pwd)
        print("Posted pwd....")
        #print self.request.text
        self.comment_on()
        
    def comment_on(self):
        #not succeed
        self.content = 'hey, you are good!'
        self.comment_url = 'http://blog.csdn.net/gt11799/comment/submit?id=' + self.article
        self.contents = {
            'commentid':'',
            'content':self.content,
            'replyld':''
        }
        print self.contents
        self.request = requests.post(self.url, headers=self.header, cookies=self.request.cookies, data=self.contents)
        print self.request.text
           
        
if __name__ == '__main__':
    article_list = ['39255873', ]
    while True:
        spider = CsdnSpider('user', 'password', article_list)
        spider.login_csdn()
        time.sleep(600)
