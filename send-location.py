#! /usr/bin/env python3
#coding: utf-8
#
import os
import threading
import time
import sys
import serial
import urllib.parse
import urllib.request
import lcd_i2c as lcd
import netifaces

#from micropy_gps import micropyGPS
import micropyGPS
#from output_csv import write_position

gps = micropyGPS.MicropyGPS()

# 出力のフォーマットは度数とする
gps.coord_format = 'dd'

url = 'http://agri-eye.bpes.kyushu-u.ac.jp/sss/api/insert_data.php'

args = sys.argv
ipa  = netifaces.ifaddresses('eth0')[2][0]['addr']

def run_gps(): 
    """
    GPSモジュールを読み、GPSオブジェクトを更新する
    :return: None
    """ 

    s = serial.Serial('/dev/ttyACM0', 115200, timeout=10)

    # 最初の1行は中途半端なデーターが読めることがあるので、捨てる
    s.readline()

    while True:

        # GPSデーターを読み、文字列に変換する
        sentence = s.readline().decode('utf-8')  

        # 先頭が'$'でなければ捨てる
        if sentence[0] != '$': 
            continue

        # 読んだ文字列を解析してGPSオブジェクトにデーターを追加、更新する
        for x in sentence: 
            gps.update(x)


# 上の関数を実行するスレッドを生成
gps_thread = threading.Thread(target=run_gps, args=())

gps_thread.daemon = True

# スレッドを起動
gps_thread.start()  

lat = 0.0
lon = 0.0

while True:

    # ちゃんとしたデーターがある程度たまったら出力する
    if gps.clean_sentences > 20:
        h = gps.timestamp[0] if gps.timestamp[0] < 24 else gps.timestamp[0] - 24
        dat = '{0:4d}/{1:02d}/{2:02d}'.format((gps.date[2]+2000),gps.date[1],gps.date[0])
        utc = "{0} {1:02d}:{2:02d}:{3:04.1f}".format(dat,h,gps.timestamp[1],gps.timestamp[2])
        lat = gps.latitude[0]
        lon = gps.longitude[0]
        alt = gps.altitude
        spd = gps.speed[2]
        #  print("{0},{1:2.8f},{2:2.8f},{3:f},{4:f}".format(utc,lat,lon,alt,spd))
        devid = 1
        gisval = {}
        gisval = {'T':'GPS','ID':devid,'UTC':utc,'LAT':lat,'LON':lon,'ALT':alt,'SPD':spd}
        params  = urllib.parse.urlencode(gisval)
        #  print(params)
        urlreq = urllib.request.Request('{}?{}'.format(url,params))
        with urllib.request.urlopen(urlreq) as urlresponse:
            the_page = urlresponse.read()
            #10秒に1回実行するように
    t = "{0:5.3f}N {1:5.3f}E".format(lat,lon)
    lcd.lcd_string(t,lcd.LCD_LINE_2)
    time.sleep(5.0)
    t = "{0:16}".format(ipa)
    lcd.lcd_string(t,lcd.LCD_LINE_2)
    time.sleep(5.0)

