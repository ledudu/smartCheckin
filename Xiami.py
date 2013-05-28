#!/usr/bin/env python
#-*- coding: utf-8 -*-
import datetime

try:
    import requests
except ImportError:
    print ImportError
    print "please try 'sudo pip install requests' to fix it !"

try:
    from bs4 import BeautifulSoup
except ImportError:
    print ImportError
    print "please try 'sudo apt-get install python-bs4' to fix it !"


class Xiami:

    """auto checkin for Xiami Music"""
    email = ''
    password = ''
    login_url = "http://www.xiami.com/member/login"
    main_url = "http://www.xiami.com"
    checkin_url = "http://www.xiami.com/web/checkin/id/"
    user_agent = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4"
    headers = {'User-Agent': user_agent}
    post_headers = {'User-Agent': user_agent,
                    'Referer': login_url}
    checkin_headers = {'User-Agent': user_agent,
                       'Referer': "http://www.xiami.com/web"}
    xiami_session = {}
    main_soup = {}

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.xiami_session = requests.Session()
        self.main_soup = BeautifulSoup()
        print datetime.datetime.now(), " : start 'Xiami' checkin for ", self.email

    def login(self):
        begin = self.xiami_session.get(self.main_url, headers=self.headers)
        print begin.content
        login_info = {
            "email": self.email,
            "password": self.password,
            "done": self.main_url,
            "submit": "登 录"
        }
        self.xiami_session.post(
            self.login_url, data=login_info, headers=self.post_headers)
        main_req = self.xiami_session.get(self.main_url, headers=self.headers)
        self.main_soup = BeautifulSoup(main_req.content)
        drop_tag = self.main_soup.find('div', attrs={"class": "more_dropInn"})
        if drop_tag:
            # 得到个人签到的URL地址
            # 得到块中一个href对应的地址，再提取用户ID
            self.checkin_url = self.checkin_url + \
                drop_tag.a.get("href").split('/')[-1]
            return True
        else:
            print datetime.datetime.now(), " : Xiami login failed for ", self.email
            return False

    def unchecked(self):
        #print self.main_soup
        raw_input("...")
        checkin_text = self.main_soup.find('a', attrs={
                                           'class': "checkin text", 'id': "check_in"})
        if checkin_text:
            return True
        else:
            print datetime.datetime.now(), " : Xiami has already checked in ! \n"
            return False

    def checkin(self):
        checkin_req = self.xiami_session.get(
            self.checkin_url, headers=self.checkin_headers)
        if checkin_req.status_code == requests.codes.ok:
            print datetime.datetime.now(), " : Xiami checkin successfully ! \n"
        else:
            print datetime.datetime.now(), " : Xiami checkin failed with ", self.email, " ! \n"

    def run(self):
        if self.login():
            if self.unchecked():
                self.checkin()
