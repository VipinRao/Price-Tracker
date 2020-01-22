from flask import Flask
import requests
import json
from bs4 import BeautifulSoup
import smtplib  #simple mail transfer protocol smtp
import time

URL="https://www.flipkart.com/adnet-laptop-power-cable-1-8m-cord/p/itmeteyhhg7mu2hn?pid=ACCETEYHY6EYDC75&lid=LSTACCETEYHY6EYDC7572QN5W&marketplace=FLIPKART&cmpid=content_data-cable_8965229628_gmc_pla&tgi=sem,1,G,11214002,g,search,,272254313975,1o9,,,m,,mobile,,,,,&ef_id=CjwKCAjwx_boBRA9EiwA4kIELm6pYPSqz0eM80WAmNKH59BRKJu4K2DQa6Ex1-HxGWFfRYlnfFclrRoCFL0QAvD_BwE:G:s&s_kwcid=AL!739!3!272254313975!!!g!328372664096!&gclid=CjwKCAjwx_boBRA9EiwA4kIELm6pYPSqz0eM80WAmNKH59BRKJu4K2DQa6Ex1-HxGWFfRYlnfFclrRoCFL0QAvD_BwE"
headers={"UserAgent":'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
'''  In computing, a user agent is software (a software agent) that is acting on behalf of a user, such as a web browser that "retrieves, renders and facilitates end user interaction with Web content". An email reader is a mail user agent '''



def send_mail(url, price, title,email):
	#establish connection cleint -server with gmail
	server=smtplib.SMTP('smtp.gmail.com',587)
	server.ehlo()
	'''Extended HELO (EHLO) is an Extended Simple Mail Transfer Protocol (ESMTP) command sent by an email server to identify itself when connecting to another email server to start the process of sending an email.'''
	server.starttls()
	'''STARTTLS. STARTTLS is a command over an in clear () connection that asks to sever to upgrade the connection to encrypted () .'''
	server.ehlo()
	server.login('vipinyadav1041998@gmail.com','mgymaiktjrzwuizy')
	subject="Required price has reached!!"
	body='check link' + url + ' current price = ' + str(price)
	msg=f"Subject:{subject}\n\n{body}"
	server.sendmail('vipinyadav1041998@gmail.com',email,msg)   #first mail is from sender side and other from reciever
	print('EMAIL SEND')
	server.quit()


def check_price(url,target_price,email):
    page = requests.get(url,headers = headers)
    soup=BeautifulSoup(page.content,'html.parser')
    #print(soup.prettify())
    title=soup.find("span",{"class":"_35KyD6"}).get_text()
    price=soup.find("div",{"class":"_1vC4OE _3qQ9m1"}).get_text()
    data = price.strip()#remove space from sides
    current_price = float(data[1:])
    print(current_price)
    print(title)
    if current_price <= target_price:
        send_mail(url,current_price,title,email)
        return True
    return False
def start(arr):
    url = arr[0]
    target_price = arr[1]
    email = arr[2]
    arrival_time = arr[3]
    flag = False
    while not flag:
        time.sleep(2)
        flag = check_price(url,target_price,email) #check price for all request in that interval
        # interval_user[interval][3] += key
