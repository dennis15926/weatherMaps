#!/usr/bin/python3
#coding: utf-8
import urllib.request
from datetime import timezone,timedelta
import datetime
import os.path

#10=a;11=b;12=c
def month_to_hex(month):
    return {
        '10': 'a',
        '11': 'b',
        '12': 'c'
    }.get(str(month), str(month))


#1=01 2=02 12=12
def int_to_str(num):
    if(num<10):
        return '0'+str(num)
    else:
        return str(num)



#1=0001 2=0002 12=0012
def int_to_str2(num):
    if(num<10):
        return '000'+str(num)
    elif(num<100):
        return '00'+str(num)
    elif(num<1000):
        return '0'+str(num)
    else:
        return str(num)

#email_handler
def send_email(recipient, subject, body):
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header

    ntu_user = "b00611035"
    ntu_pwd = "n1t5u926chen"
    FROM = ntu_user+"@ntu.edu.tw"
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = MIMEText(TEXT,_subtype='plain',_charset='UTF-8')
    message['Subject'] = Header(SUBJECT, charset='UTF-8')
    message['From']=FROM
    message['To']=", ".join(TO)
    try:
        server_ssl = smtplib.SMTP_SSL("smtps.ntu.edu.tw", 465)
        server_ssl.ehlo() # optional, called by login()
        server_ssl.login(ntu_user, ntu_pwd)  
        server_ssl.sendmail(FROM, TO, message.as_string())
        #server_ssl.quit()
        server_ssl.close()
        print ('successfully sent the mail')
    except:
        print ("failed to send mail")

#fetches map of "date", which on the server is represented as date+1 eg. 1/8~1/9 represented as 1/9
def fetch_rain_map(date):
    dl_date = date + timedelta(days=1)
    
    #2018-06-22_0000.QZJ.jpg
    file_name = str(dl_date.year) + '-' + int_to_str(dl_date.month) + '-' + int_to_str(dl_date.day) + '_0000.QZJ.jpg'
    basedir = '/home/pi/weatherMaps/rain_map/'+str(date.year)+'/'+int_to_str(date.month)+'/'
    if not os.path.exists(basedir):
        os.makedirs(basedir)
    if os.path.isfile(basedir+file_name):
        return
    url = 'http://www.cwb.gov.tw/V7/observe/rainfall/Data/' + file_name
    urllib.request.urlretrieve(url, basedir+file_name)

def fetch_temp_map(date):
    for x in range(0, 2400,100):
        file_name = str(date.year)+'-'+int_to_str(date.month)+'-'+int_to_str(date.day)+'_'+int_to_str2(x)+'.GTP.jpg'
        basedir = '/home/pi/weatherMaps/temp_map/'+str(date.year)+'/'+int_to_str(date.month)+'/'+str(date.day)+'/'
        if not os.path.exists(basedir):
            os.makedirs(basedir)
        if os.path.isfile(basedir+file_name):
            continue
        url='http://www.cwb.gov.tw/V7/observe/temperature/Data/'+file_name
        urllib.request.urlretrieve(url,basedir+file_name)

try:
    current_time = datetime.datetime.now(timezone(timedelta(hours=8)))
    print(current_time)
    fetch_rain_map(current_time-timedelta(days=1))
    fetch_rain_map(current_time-timedelta(days=2))
    fetch_temp_map(current_time-timedelta(days=1))
    fetch_temp_map(current_time-timedelta(days=2))
except Exception as e:
    send_email('dennis15926@gmail.com','RainTempMaps',"RainTempMap failed with error: " + str(e))  

    
