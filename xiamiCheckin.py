#!/usr/bin/python
# encoding:utf-8

import urllib
import urllib2
import cookielib
import sys


class Login:
    login_header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4"}
    signin_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4',
        'X-Requested-With': 'XMLHttpRequest', 'Content-Length': 0, 'Origin': 'http://www.xiami.com', 'Referer': 'http://www.xiami.com/'}
    email = ''
    password = ''
    cookie = None
    cookieFile = './cookie.dat'

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.cookie = cookielib.LWPCookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        urllib2.install_opener(opener)

    def login(self):
        postdata = {"email": self.email, "password": self.password,
                    "done": "http://www.xiami.com", "submit": "%E7%99%BB+%E5%BD%95"}
        postdata = urllib.urlencode(postdata)
        print 'Logining ...'
        req = urllib2.Request(
            url="http://www.xiami.com/member/login", data=postdata, headers=self.login_header)
        res = urllib2.urlopen(req).read()
        self.cookie.save(self.cookieFile)
        res = str(res).decode('utf-8')
        print res
        if u"Email 或者密码错误" in res:
            print "Login failed due to Email or Password error..."
            sys.exit()
        else:
            print "Login Sccessfully!"

    def unchecked(self):
        print "check status ..."
        req = urllib2.Request(
            url="http://www.xiami.com", data=None, headers=self.signin_header)
        res = urllib2.urlopen(req).read()
        res = str(res).decode('utf-8')
        self.cookie.save(self.cookieFile)
        if u"<a class=\"checkin text\" id=\"check_in\" href=\"javascript:;\" title=\"\">签到得体验点<span>Check in</span></a>" in res:
            print "have not been check in ..."
            return True
        else:
            print "already checked in ..."
            return False

    def checkin(self):
        print "signing ..."
        req = urllib2.Request(
            url="http://www.xiami.com/task/signin", data=None, headers=self.signin_header)
        res = urllib2.urlopen(req).read()
        res = str(res).decode('utf-8')
        self.cookie.save(self.cookieFile)
        try:
            res = int(res)
        except ValueError:
            print "signin failed ..."
            sys.exit()
        except:
            print "signing failed due to unknown reasons ..."
            sys.exit()

        print 'signing successfully!'
        print self.email, 'have signed', res, 'days continuously...'

if __name__ == '__main__':
    user = Login("twilight.zheng@gmail.com", "zllz8374721")
    user.login()
    if user.unchecked():
        user.checkin()
