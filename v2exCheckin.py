#!/usr/bin/python
# encoding:utf-8

import urllib
import urllib2
import cookielib
import sys
import codecs


class V2EX:

    """V2EX 自动签到程序"""
    username = ''
    password = ''
    cookie = None
    cookieFile = './cookie.v2ex.dat'
    header = {
        'User-Agent': "Mozilla / 5.0 (Windows NT 6.1) AppleWebKit / 537.4 (KHTML, like Gecko) Chrome / 22.0.1229.79 Safari / 537.4",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        'accept-charset': "UTF-8,*;q=0.5",
        'accept-language': "zh-CN"
    }

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cookie = cookielib.LWPCookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        urllib2.install_opener(opener)

    def login(self):
        postdata = {"u": self.username, "p": self.password, "submit": "登入"}
        postdata = urllib.urlencode(postdata)
        print "Logining ..."
        req = urllib2.Request(
            url="http://www.v2ex.com/signin", data=postdata, headers=self.header)
        res = urllib2.urlopen(req).read()
        self.cookie.save(self.cookieFile)
        res = str(res).decode('utf-8', 'ignore')
        f = codecs.open('v2ex.html', 'w', encoding="UTF-8")
        f.write(res)
        f.close()
        if u"/member/" + self.username in res:
            print "login successfully!"
        else:
            print "login failed!"
            sys.exit()

    def checkin(self):
        postdata = {"submit": "领取 30 铜币"}
        postdata = urllib.urlencode(postdata)
        print "signing ..."
        req = urllib2.Request(
            url="https://www.v2ex.com/mission/daily", data=postdata, headers=self.header)
        res = urllib2.urlopen(req).read()
        res = str(res).decode('utf-8')
        self.cookie.save(self.cookieFile)

        if u"<div class=\"message\">已成功领取每日登录奖励</div>" in res:
            print "checked in successfully!"
        else:
            print "checkin failed!"
            sys.exit()


if __name__ == '__main__':
    user = V2EX("jinyue524", "zllz8374721")
    user.login()
    user.checkin()
