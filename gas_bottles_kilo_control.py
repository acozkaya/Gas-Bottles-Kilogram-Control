#-*-coding:utf-8-*- 

import os
import sys
import fnmatch
import MySQLdb
import logging
import time
import datetime
import serial
from twython import Twython,  TwythonError

#EN# twitSend(), this function will send a twit to consumer by gas_bottles_bot .I've got all keys from Twitter.com  
# Keys and Secret_Keys have been entered .
def twitSend():
    CONSUMER_KEY = '0NmHFBzHChasdaj9fha'
    CONSUMER_SECRET = 'PB8w1pHasdai5zECuafbPiMBJNgBAUD1sdacZh'
    ACCESS_TOKEN = "8141948333361728-tRgasdasasdasdgGJz8xOBy7b6TfsetyO"
    ACCESS_TOKEN_SECRET = "v59kijHAHXsadsd34JO7asdasdafab07lLOgbqqcUabe"
    twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    try:
	twitter.update_status( status = '#gas bottles have a critical level kg, Please change it ')
    except TwythonError as e:
	print e
	sys.exit()


#TR# İlk olarak seri port uzerinden sensorden deger alinir, mysql e kaydedilir  
#EN# firstly, we need to get data from the sensor via serial port,thus  these data is saved in mysql
def sensorGetData():
    port = serial.Serial("/dev/ttyACM0", baudrate = 9600)
    port.flushInput()
    counter = 0
    if counter < 100:
        ongoing_data = port.readline()
        ongoing _data = ongoing_data[:-2]
        kilogram = ongoing_data
        insertDB(kilogram)
        counter+=counter
    else:   
        port.close()


#TR# mysql den veriler okunur ve kritik degere gore twitSend() fonksiyonu calisir
#EN# Firstly, we need to read data from the mysql, and aslo we have a critical value for gas bottles kilo control therefore, if own gas bottles kilo are empty and/or under the critical value we have to call the twitSend() function
def readDB():    
    con = MySQLdb.connect('localhost', 'root', 'pi3', 'gas_bottles_control')
    cursor = con.cursor()
    sql = "SELECT kilo FROM `kg` ORDER BY `id` DESC"
    cursor.execute(sql)
    kilogram = cursor.fetchone()
    cursor.close()
    con.close()
    for line in kilogram:
        print line;
        if line < 4: # 4 
            twitSend()
            print "twit has been sent"
        else:
            print "gas bottles kg is enough"   
	sys.exit()	


#TR# veriler mysql'e kaydedilir .
#EN# data have been recorded to mysql 	
def insertDB(kilogram):
    sql = "INSERT INTO kg (date, time, kilo) VALUES ('%s', '%s', '%s' )" % (time.strftime("%Y-%m-%d"), time.strftime("%H:%M"), kilogram)
    con = MySQLdb.connect('localhost', 'root', 'pi3', 'gas_bottles_control')
    cursor = con.cursor()
    cursor.execute(sql)
    con.commit()
    con.close()


sensorGetData()	
readDB()
   

	
