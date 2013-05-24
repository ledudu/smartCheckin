#!/usr/bin/env python
#-*- coding: utf-8 -*-

try:
    import requests
except ImportError:
    print ImportError
    import os
    os.system("sudo pip install requests")

import time

try:
    from bs4 import BeautifulSoup
except ImportError:
    print ImportError
    import os
    os.system("sudo apt-get install python-bs4")


signin_url = "http://www.v2ex.com/signin"
award_url = "http://www.v2ex.com/mission/daily"
main_url = "http://www.v2ex.com"

user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.63 Safari/537.31"
post_headers = {"User-Agent": user_agent,
                "Referer": "http://www.v2ex.com/signin"}
headers = {"User-Agent": user_agent}
v2ex_session = requests.Session()


class V2EX:

    """auto checkin for V2EX and get rewards"""
    username = ''
    password = ''

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_login_info(self):
        v2ex_main_req = v2ex_session.get(signin_url, headers=headers)
        v2ex_main_tag = BeautifulSoup(v2ex_main_req.content)

        form_tag = v2ex_main_tag.find(
            'form', attrs={"method": "post", "action": "/signin"})
        input_once_tag = form_tag.find('input', attrs={"name": "once"})
        input_once_value = input_once_tag.attrs["value"]

        login_info = {
            "next": "/",
            "u": self.username,
            "p": self.password,
            "once": input_once_value,
            "next": "/"
        }

        return login_info

    def get_award(self):
        # login
        login_info = self.get_login_info()

        v2ex_session.post(signin_url, data=login_info, headers=post_headers)
        main_req = v2ex_session.get(main_url, headers=headers)
        main_soup = BeautifulSoup(main_req.content)
        top_tag = main_soup.find('div', attrs={"id": "Top"})
        user_tag = top_tag.find(href="/member/"+self.username)
        if not user_tag:
            print "login failed !"
            return

        # check for award info
        award_tag = main_soup.find(href="/mission/daily")
        if not award_tag:
            print "You have got the award already !"
            return

        # get award if haven't got it
        get_award_req = v2ex_session.get(award_url, headers=headers)
        get_award_soup = BeautifulSoup(get_award_req.content)
        button_tag = get_award_soup.find('input', attrs={'type': 'button'})
        click_href = button_tag.attrs["onclick"]
        first_dot_index = click_href.find("'")
        last_dot_index = click_href.find("'", first_dot_index + 1)
        click_url = main_url + click_href[first_dot_index + 1: last_dot_index]
        time.sleep(80)
        award_req = v2ex_session.get(click_url, headers=headers)
        award_soup = BeautifulSoup(award_req.content)
        result_tag = award_soup.find('div', class_="message")
        print result_tag.string

if __name__ == '__main__':
    user = V2EX("jinyue524", "zllz8374721")
    user.get_award()
    print "v2ex check in done! \n\n"
