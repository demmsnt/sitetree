#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""Различные методы отправки почты"""
GMAIL = 'smtp.gmail.com'
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import os
import logging

def createMessage(fro, to, subject, text, files=None):
    if files is None:
        files=[]

    assert type(to) == list
    assert type(files) == list
    #fro = FROM

    msg = MIMEMultipart()
    msg['From'] = fro
    msg['To'] = COMMASPACE.join(to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    text_message = MIMEText(text)
    text_message.set_charset('UTF-8')
    msg.attach(text_message)

    for file in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(file, "rb").read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"'
                       % os.path.basename(file))
        msg.attach(part)
    return msg


def sendSMTP(fro, to, subject, text, files=None, server=None):
    """Отправка почты через SMTP без авторизации:
        sendMail(
                ["dem@masternetdon.ru"],
                "test","Проверка",
                ['aaa.txt','bbb.jpg']
            )
    """
    msg = createMessage(fro, to, subject, text, files=files)
    smtp = smtplib.SMTP(server)
    smtp.sendmail(fro, to, msg.as_string())
    smtp.close()


def sendGmail(fro, to, subject, text, files=None, username='', password=''):
        """Отправка через гугл с применением одноразового пароля"""
 # fromaddr = 'fromuser@gmail.com'
 # toaddrs  = 'touser@gmail.com'
 # msg = 'There was a terrible error that occured and I wanted you to know!'
 # Credentials (if needed)
 # username = 'username'
 #  password = 'password'
        logger = logging.getLogger()
        # The actual mail send
        msg = createMessage(fro, to, subject, text, files=files)
        logger.debug('Create smtp instance')
        server = smtplib.SMTP(GMAIL)
        server.starttls()
        logger.debug('login')
        server.login(username, password)
        logger.debug('send')
        server.sendmail(fro, to, msg.as_string())
        logger.debug('quit')
        server.quit()
        
