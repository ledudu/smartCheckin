#!/usr/bin/env python
#-*- coding: utf-8 -*-
# import datetime
import smtplib
import email.mime.text
import sys
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
        Errors = ""
        for each in lines:
            if each.find("failed") != -1:
                Errors += each
        if Errors != "":
            self.send_mail(Errors)

    def send_mail(self, text):
        print "Connecting Gmail Server ..."
        smtp = smtplib.SMTP(self.host, self.port, timeout=25)
        smtp.starttls()

        try:
            print 'Logging Gmail Server ...'
            smtp.login(self.username, self.password)
        except:
            print "Login Error *****"
            sys.exit()

        msg = email.mime.text.MIMEText(text)
        msg['From'] = self.username
        msg['To'] = self.target
        msg['Subject'] = "SmartCheckin Error !"
        print msg.as_string()
        smtp.sendmail(self.username, self.target, msg.as_string())
        sleep(5)
        smtp.quit()
