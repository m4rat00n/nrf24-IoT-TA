#!/usr/bin/python
# -*- coding: utf-8 -*-
#

import sys
sys.path.insert(0, '/home/pi/lib_nrf24')
sys.path.insert(0, '/home/pi/decryption/dekrip')


import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
from lib_nrf24 import NRF24
from post_data import upload_data
#from SimonCipher_dec import decrypt_dt
from SimeckCipher_dec import decrypt_dt
#from SpeckCipher_dec import decrypt_dt
import time
from datetime import datetime
import spidev
import re



pipes = [[0xE0, 0xE0, 0xF1, 0xF1, 0xE0], [0xF1, 0xF1, 0xF0, 0xF0, 0xE0]]

radio2 = NRF24(GPIO, spidev.SpiDev())
radio2.begin(0, 25)

radio2.setRetries(15,15)

radio2.setPayloadSize(32)
radio2.setChannel(0x76)
radio2.setDataRate(NRF24.BR_1MBPS)
radio2.setPALevel(NRF24.PA_MAX)

radio2.setAutoAck(True)
radio2.enableDynamicPayloads()
radio2.enableAckPayload()

radio2.openWritingPipe(pipes[0])
radio2.openReadingPipe(1, pipes[1])

radio2.startListening()
radio2.stopListening()

radio2.printDetails()

radio2.startListening()

c=1
while True:
  #block = int(input('input Block Size: '))
   #block = 32
   #key = 64
   jrk = 0
  #key = int(input('input Key Size: '))
  #jrk = int(input("Enter Distance: "))
  #for i in range(0,40):
   try:
    akpl_buf = [1]
    #akpl_buf2 = [2]
    while not radio2.available(0):
        time.sleep(1/100)

    recv_buffer = []
    radio2.read(recv_buffer, radio2.getDynamicPayloadSize())
    radio2.writeAckPayload(1, akpl_buf, len(akpl_buf))
    header = recv_buffer[0]
    del recv_buffer[0]
    str_msg = ''.join(map(chr, recv_buffer))
    if '0x' in str_msg or str_msg.upper().isupper() == True:
        #print('log if luar')
        continue
    else:
        #get received time
        t = datetime.now()
        mhrs = int(format(t, '%H'))*3600*1000000
        mmnt = int(format(t, '%M'))*60*1000000
        msec = int(format(t, '%S'))*1000000
        ms = int(format(t, '%f'))
        time_recv= mhrs+mmnt+msec+ms
        #print(time_recv)

        #regex for time
        retime_send = re.compile("@(\d{6,12})")
        time_send = retime_send.search(str_msg)
        time_send_fix = int(time_send.group(1))
        #print(time_send_fix)

        #regex for packet total
        retotal_pckt = re.compile("> (\d{1,2})")
        total_pckt = retotal_pckt.search(str_msg)
        packet = int(total_pckt.group(1))

        print ("Total Packet: ") ,
        print (str(packet))
        time.sleep(1)
   
        pkt_count = 0
        str_msg1 = '' 
        i = 1
        tot_pkt = int(packet)
        while i<=tot_pkt:
            while not radio2.available(0):
                time.sleep(1/100)

            recv_buffer1 = []
            radio2.read(recv_buffer1, radio2.getDynamicPayloadSize())
            radio2.writeAckPayload(1, akpl_buf, len(akpl_buf))

            head = recv_buffer1[0]
            del recv_buffer1[0]

            id = recv_buffer1[0]
            del recv_buffer1[0]

            #Proccess the message
            act_cek = ''.join(map(chr, recv_buffer1))
            if header == head:
              if '0x' in act_cek or act_cek.upper().isupper() == True and id == i:
                str_msg1 = str_msg1+''.join(map(chr, recv_buffer1))
                cek = True
                pkt_count += 1
                i += 1
                #print('masuk if dalam')
              else:
                #print('else dalam')
                cek = False
                break
            time.sleep(1)
        #print(cek)
        if cek == True:
            enc_msg_len = len(str_msg1)
            print ("Message Received: "+str(str_msg1))
            message = decrypt_dt(str_msg1,block,key)
            msg_len = len(message)
            #code for upload and regex for get the data
            #upload for the data with encryption
            upload_data(tot_pkt,pkt_count,message, time_recv, enc_msg_len, msg_len, jrk, time_send_fix)
        else:
            enc_msg_len=len(str_msg1)
            upload_data(tot_pkt,pkt_count,'null', time_recv,enc_msg_len,0,jrk,time_send_fix) 

   except ValueError as err:
    print(err)
    enc_msg_len=len(str_msg1)
    upload_data(tot_pkt,pkt_count,'null', time_recv,enc_msg_len,0,jrk,time_send_fix)

   except IOError as err:
    print(err)
    enc_msg_len=len(str_msg1)
    upload_data(tot_pkt,pkt_count,'null', time_recv,enc_msg_len,0,jrk,time_send_fix)

   except AttributeError as err:
    print(err)
    enc_msg_len=len(str_msg1)
    upload_data(tot_pkt,pkt_count,'null', time_recv,enc_msg_len,0,jrk,time_send_fix)
   except IndexError as err:
    print(err)
    enc_msg_len=len(str_msg1)
    upload_data(tot_pkt,pkt_count,'null', time_recv,enc_msg_len,0,jrk,time_send_fix)
