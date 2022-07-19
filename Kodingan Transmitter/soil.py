#!/usr/bin/python3
import spidev
import os
import time

spi = spidev.SpiDev()
spi.open(0,1)
spi.max_speed_hz=1000000
max_val=460.0 #max value

def soil_count():
  value = spi.xfer([1, 128, 0])
  if (0<=value[1]<=3):
    valueS = 1023 - ((value[1]*256)+value[2])
    data_value = ((valueS/max_val)*100)
    #if data_value > 100:
    #  data_value = 100.00
    return data_value
  time.sleep(0.2)
