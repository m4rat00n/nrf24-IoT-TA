#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#lsusb to check device name
#dmesg | grep "tty" to find port name

import serial,time
import re
import sys

msg_dist=0
#def get_esp():
while True:
  with serial.Serial('/dev/ttyUSB0', 115200, timeout = 0.1) as ESP:
    time.sleep(0.1)
    if ESP.isOpen():
      #print("{} connected!".format(arduino.port))
      while True:
         #print('1')
         while ESP.inWaiting()==0: 
            #print('5')
            pass
         if ESP.inWaiting()>0:
           try:
            #print('2')
             ser1=ESP.readline()
             ser = ser1.decode('UTF-8')
             print(ser)

            #Regex
            #vol_a_regex = re.compile('VoltageA: \d{1,6}.\d{1,3}')
            #current_a_regex = re.compile('CurrentA: -?\d{1,6}.\d{1,2}')
            #power_a_regex = re.compile('PowerA: \d{1,6}.\d{1,2}')

            #current_a = current_a_regex.search(ser)
            #vol_a = vol_a_regex.search(ser)
            #power_a = power_a_regex.search(ser)
            
            #vol_a = vol_a.group()
            #current_a = current_a.group()
            #power_a = power_a.group()
            
            #print(vol_a+' V')
            #print(current_a+' mA')
            #print(power_a+' mW')
             ESP.flushInput()
             time.sleep(0.1)
             if 'INA 219 A' in ser:
                print('OK')
                #return ser

           except ValueError as err:
             print(err)
             break

           except IOError as err:
             print(err)
             break
