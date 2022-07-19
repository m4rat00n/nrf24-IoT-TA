import requests
import re

def upload_data(pkt_sn,pkt_rec,msg,time_recv,chiper_len,plain_len,jarak,time_send):
    ENDPOINT = "http://localhost/addData.php?function=add_data"
    ENDPOINT2 = "http://localhost/addData.php?function=update_data"
    
    if msg == 'null':
       delay = (int(time_recv)-int(time_send))/1000000+0.02
       angin_f = 0.0
       hujan_f = 0.0
       temp_f = 0.0
       hum_f = 0.0
       soil_f = 0.0
    else:
       #retime_send = re.compile("d(\d{6,12})")
       reangin = re.compile("v(\d{1,2}.\d{1,3})")
       rehujan = re.compile("r(\d{1,3}.\d{0,2})")
       retemp = re.compile("T(\d{1,2}.\d{1,2})")
       rehum = re.compile("H(\d{1,3}.\d{1,2})")
       resoil = re.compile("s(\d{1,3}.\d{1,2})")

       #time_send = retime_send.search(msg)
       angin = reangin.search(msg)
       hujan = rehujan.search(msg)
       temp = retemp.search(msg)
       hum = rehum.search(msg)
       soil = resoil.search(msg)

       angin_f = float(angin.group(1))
       hujan_f = float(hujan.group(1))
       temp_f = float(temp.group(1))
       hum_f = float(hum.group(1))
       soil_f = float(soil.group(1))

       delay_ms = int(time_recv)-int(time_send)
       delay = delay_ms/1000000+0.02
       if soil_f > 100:
          soil_f = 100
    data = {'pckt_send':pkt_sn,
            'pckt_recv':pkt_rec,
            'chiper_len':chiper_len,
            'plain_len':plain_len,
            'delay':delay,
            'kec_angin':angin_f,
            'curah_hujan':hujan_f,
            'Temp':temp_f,
            'Humidity':hum_f,
            'soil_mois':soil_f,
            'Jarak':jarak}

    data_update = {'delay':delay,
                   'kec_angin':angin_f,
                   'curah_hujan':hujan_f,
                   'temp':temp_f,
                   'humidity':hum_f,
                   'soil_mois':soil_f}

    res = requests.post(url = ENDPOINT, data = data)
    #extract the response
    print("Response post: %s"%res.text)

    response = requests.post(url = ENDPOINT2, data=data_update)
    print('Response update: %s'%response.text)
