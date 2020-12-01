#! /usr/bin/python3
#coding: utf-8
#
#  Version 1.00
#     <horimoto@holly-linux.com>
#
import os
import threading
import time
import sys
import serial
import urllib.parse
import urllib.request
import lcd_i2c as lcd


url = 'http://agri-eye.bpes.kyushu-u.ac.jp/sss/api/insert_data.php'

try:
    s = serial.Serial('/dev/ttyUSB0',115200,timeout=1)
except serial.serialutil.SerialException:
    print("NO Serial ttyUSB0")
    quit()

s.readline()
lcd.lcd_string("ssdata A-OK",lcd.LCD_LINE_1)
while(True):
    a = s.readline().decode().rstrip()
    b = a.split(',')
    if (b[0]=='DT'):
        devid = 1
        gisval = {}
        gisval = {'T':'SSS','ID':devid,'CNT':b[1],'DWX':b[2],'DWY':b[3],'DWZ':b[4],'WX':b[5],'WY':b[6],'WZ':b[7]}
        params  = urllib.parse.urlencode(gisval)
        # print(params)
        urlreq = urllib.request.Request('{}?{}'.format(url,params))
        with urllib.request.urlopen(urlreq) as urlresponse:
            the_page = urlresponse.read()
            x = "SEND {0:>9}".format(b[1])
            lcd.lcd_string(x,lcd.LCD_LINE_1)
            time.sleep(1.0)
        x = "SS=[{0:>3},{1:>3},{2:>3}]".format(b[2],b[3],b[4])
        lcd.lcd_string(x,lcd.LCD_LINE_1)
