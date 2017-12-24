#!/usr/bin/python

import mysql.connector
import ConfigParser
from datetime import datetime

config = ConfigParser.RawConfigParser()
config.read('dogeanalytics.cfg')

user = config.get('Database', 'user')
password = config.get('Database', 'password')
hostname = config.get('Database', 'hostname')
dbName = config.get('Database', 'database')

date_format = "%Y-%m-%d %H:%M:%S"
add_new_best = ("INSERT IGNORE INTO new_best_block "
               "(hash, height, tx_count, date, version) "
               "VALUES (%(hash)s, %(height)s, %(tx_count)s, %(date)s, %(version)s)")

cnx = mysql.connector.connect(user=user, password=password,
                              host=hostname,
                              database=dbName)
cursor = cnx.cursor()

versionsFile = open("/mnt/versions.txt", "r")
for line in versionsFile:
     parts = line.split(" ")
     block_hash = ''
     height = -1
     tx_count = -1
     date = ''
     version = ''
     for partIdx in range(0, len(parts)):
          part = parts[partIdx]
          if "=" not in part:
              continue
          keyValue = part.split("=")
          if (keyValue[0] == "best"):
              block_hash = keyValue[1]
          elif (keyValue[0] == "height"):
              height = keyValue[1]
          elif (keyValue[0] == "tx"):
              tx_count = keyValue[1]
          elif (keyValue[0] == "date"):
              date = datetime.strptime(keyValue[1] + " " + parts[partIdx + 1], date_format)
          elif (keyValue[0] == "version"):
              version = keyValue[1]
     best_data = {
          'hash': block_hash,
          'height': height,
          'tx_count': tx_count,
          'date': date,
          'version': version
     }
     cursor.execute(add_new_best, best_data)
     cnx.commit()

cursor.close() 
cnx.close()
