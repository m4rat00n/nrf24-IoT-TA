#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Example program to send packets to the radio link
#


import RPi.GPIO as GPIO
import sys
GPIO.setmode(GPIO.BCM)
sys.path.insert(0,'/home/pi/lib_nrf24')
from lib_nrf24 import NRF24
import time
import timeit
import spidev
from datetime import datetime

def times():
    time= datetime.now()
    mhrs=int(format(time, '%H'))*3600*1000000
    mmnt=int(format(time, '%M'))*60*1000000
    msec=int(format(time, '%S'))*1000000
    ms=int(format(time, '%f'))
    time_send=mhrs+mmnt+msec+ms
    return time_send

def kirim(message): 
    #start=timeit.default_timer()
    pipes = [[0xE0, 0xE0, 0xF1, 0xF1, 0xE0], [0xF1, 0xF1, 0xF0, 0xF0, 0xE0]]

    radio = NRF24(GPIO, spidev.SpiDev())
    radio.begin(0, 25)
    time.sleep(1)
    radio.setRetries(15,15)
    radio.setPayloadSize(32)
    radio.setChannel(0x76)

    radio.setDataRate(NRF24.BR_1MBPS)
    radio.setPALevel(NRF24.PA_MAX)
    radio.setAutoAck(True)
    radio.enableDynamicPayloads()
    radio.enableAckPayload()


    radio.openWritingPipe(pipes[1])
    radio.openReadingPipe(1, pipes[0])
    radio.printDetails()
    
    sendMessage = list(message)  #the message to be sent
    length=len(sendMessage)
    tot_pkt=0
    pkt_id=1
    split_msg = [sendMessage[i:i+30] for i in range(0, length, 30)]
    for x in split_msg:
        x[:0]=["1",pkt_id]
        tot_pkt=tot_pkt+1
        pkt_id += 1
    #tot_pkt=list(str(tot_pkt))

    while True:
        # send a packet to receiver
        send_time = times()
        msg_pckt = '1@'+str(send_time)+'> '+str(tot_pkt)
        msg_pckt = list(msg_pckt)
        radio.write(msg_pckt)
        
        print ("Send Total Packet :"),
        print (tot_pkt)
        #time.sleep(5)
        # did it return with a payload
        if radio.isAckPayloadAvailable():
            pl_buffer=[]
            radio.read(pl_buffer, radio.getDynamicPayloadSize())
            print ("Received back: "),
            print (pl_buffer)
        else:
            print ("Received: Ack only, no payload")
        time.sleep(3)
        #stop=timeit.default_timer()
        for pkt in split_msg:
            radio.write(pkt)
            print("Message : ")
            print(pkt)
            #time.sleep(5)
            if radio.isAckPayloadAvailable():
                pl_buffer=[]
                radio.read(pl_buffer, radio.getDynamicPayloadSize())
                print ("Received back: ")
                print (pl_buffer)
            else:
                print ("Received: Ack only, no payload")
            time.sleep(3)
        #print("masuk")
        #print(stop-start)
        break

