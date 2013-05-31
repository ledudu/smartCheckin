#!/usr/bin/env python
#-*- coding: utf-8 -*-
# import datetime
import smtplib
import email.mime.text
from time import sleep


class Notify_Admin:

    """docstring for Notify_Admin"""
    target = ""
    username = ''
    password = ''
    host = "smtp.gmail.com"
    port = 587

    def __init__(self, target, username, password):
        self.target = target
        self.username = username
        self.password = password

    def check_error(self, filename):
        lines = file(filename, 'r').readlines()
        for line in lines:
            print line

    def send_mail(self, text):
        print "Connecting Gmail Server ..."
        smtp = smtplib.SMTP(self.host, self.port, timeout=25)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        try:
            print 'Logging Gmail Server ...'
            smtp.login(self.username, self.password)
        except:
            print "Login Error *****"

        msg = email.mime.text.MIMEText(text)
        msg['From'] = self.username
        msg['To'] = self.target
        msg['Subject'] = "SmartCheckin Error !"
        print msg.as_string()
        smtp.sendmail(self.username, self.target, msg.as_string())
        sleep(5)
        smtp.quit()

if __name__ == '__main__':
    mail = Notify_Admin(
        "twilight.zheng@gmail.com", "samien.zheng@gmail.com", "Twilight21")
    mail.check_error("log")
