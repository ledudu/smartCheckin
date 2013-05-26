#!/usr/bin/env python
#-*- coding: utf-8 -*-
import datetime
import time

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
    checkin_url = "http://www.xiami.com/task/signin"
    user_agent = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4"
    headers = {'User-Agent': user_agent}
    post_headers = {'User-Agent': user_agent,
                    'Referer': login_url}
    xiami_session = requests.Session()
    main_soup = BeautifulSoup()

    def __init__(self, email, password):
        self.email = email
        self.password = password
        print datetime.datetime.now(), " : start 'Xiami' checkin for ", self.email

    def login(self):
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
        logout_tag = drop_tag.find(href="/member/logout")
        if not logout_tag:
            print datetime.datetime.now(), " : Xiami login failed for ", self.email
            return False
        else:
            return True

    def unchecked(self):
        coins_tag = self.main_soup.find('div', attrs={'id': "ys_coins"})
        checkin_text = coins_tag.find('a', attrs={
                                      'class': "checkin text", 'id': "check_in"})
        if not checkin_text:
            print datetime.datetime.now(), " : Xiami has already checked in !"
            return False
        else:
            return True

    def checkin(self):
        time.sleep(80)
        checkin_req = self.xiami_session.get(
            self.checkin_url, headers=self.headers)
        if checkin_req.status_code == requests.codes.ok:
            print datetime.datetime.now(), " : Xiami checkin successfully ! \n"
        else:
            print datetime.datetime.now(), " : Xiami checkin failed with ", self.email, " ! \n"

    def run(self):
        if self.login() and self.unchecked():
            self.checkin()
