#!/usr/bin/env python
from bs4 import BeautifulSoup
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

WEB_URL = 'https://www.flipkart.com/apple-iphone-xr-black-64-gb/p/itmf9z7zxu4uqyz2?pid=MOBF9Z7ZPHGV4GNH&srno=s_1_1&otracker=search&otracker1=search&lid=LSTMOBF9Z7ZPHGV4GNH9IFADQ&fm=SEARCH&iid=a6446318-92aa-4974-aa37-deb2b8639780.MOBF9Z7ZPHGV4GNH.SEARCH&ppt=sp&ppn=sp&ssid=1xw8uxhhq80000001569760965489&qH=868ed02c58567157'

#Format Phone Price from $50,000 -->> 50000 in our case Rs. symbol in case of $
def formatPhonePriceValue(priceValue):
    arrayInitial = priceValue.split(",")
    secondValueOfArray = str(arrayInitial[1])
    firstValueArray = list(arrayInitial[0])
    firstValueArray.pop(0)
    firstValueOfArray = str("".join(firstValueArray))
    finalPriceValue = int(str(firstValueOfArray)+str(secondValueOfArray))
    checkPriceLogic(finalPriceValue)

#Price Logic
def checkPriceLogic(price):
    if (price >= 48000 and price <=49000):
        sendEmailAlertToBoss("Price Fell Down",price)

#Send Email Logic
def sendEmailAlertToBoss(message,price):
    bcc = "ENTER DESTINATION EMAIL ID"
    msg = MIMEMultipart()
    fromaddr = 'ENTER FROM EMAIL ID HERE'
    msg['subject'] = f"{message}"
    text = MIMEText(f'Hi Mayank, <br> <h3>{message}</h3> <br> You Can See here: <a href="{WEB_URL}"">iPhone XR</a> <br><br> Thank You <br> Your Lovely Bot','html')
    msg.attach(text)
    
    SENDER_EMAIL = 'YOUR GMAIL ID HERE FOR AUTHENTICATION'
    SENDER_PASSWORD = 'YOUR GMAIL PASSWORD HERE FOR AUTHENTICATION'

    s = smtplib.SMTP('smtp.gmail.com',587) #We are using GMAIL as our email client.
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(SENDER_EMAIL, SENDER_PASSWORD)
    s.sendmail(fromaddr, bcc, msg.as_string())
    s.quit()

#Main point to Enter the Program
#Got the Entire HTML Content of the website
source = requests.get(WEB_URL).content
soup = BeautifulSoup(source, 'html.parser')
try:
    for iphoneXR in soup.find_all('div',class_='_1uv9Cb'):
        priceValue = iphoneXR.find('div',class_='_1vC4OE _3qQ9m1').text
        formatPhonePriceValue(priceValue)
except AttributeError as identifier:
    pass