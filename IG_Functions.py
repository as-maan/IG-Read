# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 12:54:15 2018

@author: amaan
"""

import datetime
import ast
import serial
import random

import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
    

def serial_read():
    ser = serial.Serial('/dev/ttyUSB1', 19200, timeout=0.1)    
    ser.apply_settings
    if ser.isOpen():
        ser.write("#01RD\r")
        pressure = repr(ser.read(16))
        pressure = list(pressure)
        pressure = pressure[5:13]
        pressure = ''.join(pressure)
        if (pressure == 'SYNTX ER' or pressure == ''):
            pressure = float('nan')
        else:
            pressure = ast.literal_eval(pressure)
    return {'val':pressure}
    
def get_date():
    now = datetime.datetime.now()
    yyyy = str(now.year)
    mm = str(now.month)
    dd = str(now.day)
    date = dd+mm+yyyy
    return {'date':date}

def get_time():
    now = datetime.datetime.now()
    hr = now.hour
    min = now.minute
    sec = now.second
    time = str(hr)+':'+str(min)+':'+str(sec)
    return {'time':time, 'sec':sec}

def send_email(user, file, recipient, subject, body):

    msg = MIMEMultipart()
    msg['From'] = user
    msg['To'] = recipient
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(body))
    files=[file]
    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
            # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)
    server = smtplib.SMTP()
    server.connect('smtp.gmail.com',587)
    server.starttls()
    server.login(user,"huvrqpubstycatju")
    server.sendmail(user,recipient, msg.as_string())
    server.quit()
