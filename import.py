#!/usr/bin/python

import mysql.connector
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('dogeanalytics.cfg')

user = config.get('Database', 'user')
password = config.get('Database', 'password')
hostname = config.get('Database', 'hostname')
dbName = config.get('Database', 'database')

add_new_best = ("INSERT IGNORE INTO new_best_block "
               "(hash, height, tx_count, date, version) "
               "VALUES (%s, %d, %d, %s, %d)")

cnx = mysql.connector.connect(user=user, password=password,
                              host=hostname,
                              database=dbName)

versionsFile = open("versions.txt", "r")
for line in versionsFile:
     parts = line.split(" ")


cnx.close()
