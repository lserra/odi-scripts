# remove_double_quotes
# Author: Laercio Serra
# Created on: 10/07/2016
# Project: License Ticket
# Version 1: script to treatment of the file, removing all characteres similar a double quotes

import os, re

file='/u01/integracao/MDM/Ticketing/CUSTOMER_DATA_start.csv'

fp=open(file,'r')
ft=open('/u01/integracao/MDM/Ticketing/All/CUSTOMER_DATA.csv','w')

line=fp.readline()

while line:
        line = line.replace('\"','')
        ft.write(line)
        line=fp.readline()

fp.close()
ft.close()
