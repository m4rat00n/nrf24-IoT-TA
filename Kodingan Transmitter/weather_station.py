from gpiozero import Button
import Adafruit_DHT
import math
import time
from datetime import datetime
from nrf24send import kirim
from soil import soil_count
import timeit
import sys

sys.path.insert(0, '/home/pi/encryption/Encryption')
from SimeckCipher_enc import encrypt_dt
#from SpeckCipher_enc import encrypt_dt
#from SimonCipher_enc import encrypt_dt
#DHT22 SENSOR
DHT_SENSOR = Adafruit_DHT.DHT22
dht_pin = 17

#WIND SENSOR
wind_count = 0
wind_interval=10.00 #second
radius_m = 0.1 #meter
calibration_value = 2.0
ms_to_kmh = 3.6

#RAIN SENSOR
#Luas corong 5,5 cm x 3,5 cm = 19,25 cm2
#Kalibrasi dengan menuangkan 10mL air dan habis dengan 7 tip. 10mL/7 = 1,42mL p>
#nilai 1 tip = 1,42/19,25 = 0,07cm atau 0,70mm
bucket_size = 0.70 #mm
rain_count = 0
time_2_reset_rain = 86400 #sec
start_rain_time = datetime.now()
rainfall=0.00

def spin():
   global wind_count 
   wind_count = wind_count + 1
   #print(wind_count)

def calculate_speed(time_sec):
   global wind_count
   circum_m = (2*math.pi)*radius_m
   rotasi = wind_count / time_sec #rps
   velocity_ms = circum_m * rotasi #m/s
   velocity_kmh = velocity_ms*ms_to_kmh #km/h
   return velocity_kmh * calibration_value

def reset_wind():
   global wind_count
   wind_count = 0

def bucket_tipped():
   global rain_count
   global rainfall
   rain_count = rain_count + 1
   rainfall = rain_count * bucket_size
   rainfall = "{:.2f}".format(rainfall)
   print("curah hujan :"+str(rainfall)+" mm")

def reset_rain():
   global rain_count
   rain_count = 0

def humi_temp():
   global hum, temp
   hum = 0
   temp = 0
   hum, temp = Adafruit_DHT.read_retry(DHT_SENSOR, dht_pin)
   if hum is not None and temp is not None:
      hum = "{1:0.1f}".format(temp,hum)
      temp = "{0:0.1f}".format(temp,hum)
      print("Temp = {} dan Humidity = {}".format(temp,hum))
   else:
      print("Gagal untuk membaca sensor")

def times():
   time= datetime.now()
   mhrs=int(format(time, '%H'))*3600*1000000
   mmnt=int(format(time, '%M'))*60*1000000
   msec=int(format(time, '%S'))*1000000
   ms=int(format(time, '%f'))
   time_send=mhrs+mmnt+msec+ms
   return time_send

wind_speed_sensor = Button(5)
rain_sensor = Button(6)
wind_speed_sensor.when_pressed = spin
rain_sensor.when_pressed = bucket_tipped

if __name__ == '__main__':
   try:
      while True:
       #block=int(input('input block size: '))
       #key=int(input('input key size: '))
       #pesan_size=int(input('input message size: '))
       #for k in range(0,40):
         #static block and key size
         block = 32
         key = 64
         pesan_size = 20
         reset_wind()
         time.sleep(wind_interval)
         humi_temp()
         soilVal=soil_count()
         soilVal="{:.1f}".format(soilVal)
         speed = calculate_speed(wind_interval)
         format_speed = "{:.3f}".format(speed)
         print("Angin: "+str(format_speed)+" km/jam")
         print("Curah Hujan: "+str(rainfall)+" mm")
         print("Kelembapan Tanah: "+str(soilVal)+" %")
         #time_send=times()
         send2recv_1 ="velocity"+ str(format_speed)+"rainfall"+str(rainfall)+"Temperature"+str(temp)+"Humidity"+str(hum)+"soil"+str(soilVal)+'n'
         #kirim(send2recv_1)

         	#code for encrypt
         enc_msg = encrypt_dt(send2recv_1,block,key,pesan_size)

         kirim(enc_msg)

         cek_rain_time = datetime.now()
         cek_reset_rain = cek_rain_time - start_rain_time
         sec_rain_time = cek_reset_rain.total_seconds()
         #print(sec_rain_time)
         if sec_rain_time >= 86400:
            reset_rain()
            start_rain_time = time.time()
 
   except KeyboardInterrupt:
      print("Measurement stopped by USER")
