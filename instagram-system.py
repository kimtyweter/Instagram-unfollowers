#!/usr/bin/env python
# coding: utf-8
import getpass # hide passward
import instaloader # get Instagram API
import pandas as pd
import time

# send email
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

# Login Instgram
print('Login Instagram account and password')

L = instaloader.Instaloader()

username = input('Instagram Account:')

password = getpass.getpass('Instagram Password:')

# email = str(input('Your email address：'))
email = '####@gmail.com'

L.login(username, password)  # (login)
profile = instaloader.Profile.from_username(L.context, username)

# Obtain followers
followers_list = []
followers_list_name = []
follow_list = []
for follower in profile.get_followers():
    followers_list.append(follower.username)
    followers_list_name.append(follower.full_name)

# Obtain followings
following_list = []
following_list_name = []
for followee in profile.get_followees():
    following_list.append(followee.username)
    following_list_name.append(followee.full_name)

# Data Processing

d = {'Followers':followers_list}
df = pd.DataFrame(d)
df['Followers_Name'] = pd.Series(followers_list_name)
df['Followings'] = pd.Series(following_list)
df['Followings_Name'] = pd.Series(following_list_name)
a = df[~df['Followings'].isin(df['Followers'])][['Followings_Name', 'Followings']].dropna()
a = a.reset_index(drop = True)
# Send email
# # Send email to user

# In[108]:

email = str(input('Your email address：'))
toaddr = username

fromaddr = "####@gmail.com" # developer email

# instance of MIMEMultipart 
msg = MIMEMultipart() 
  
# storing the senders email address   
msg['From'] = fromaddr 
  
# storing the receivers email address  
msg['To'] = email
  
# storing the subject  
msg['Subject'] = str(username)
  
# string to store the body of the mail 

body = 'Hi '+str(username)+ '. Your unfollowers analysis file is in the attachment'
  
# attach the body with the msg instance 
msg.attach(MIMEText(body, 'plain')) 
  
# open the file to be sent  
a.to_csv('unfollowers.csv', index = 0)
attachment = open("/Users/kimtyweter/Desktop/python/instagram/unfollowers.csv", "rb") 
  
# instance of MIMEBase and named as p 
p = MIMEBase('application', 'octet-stream') 
  
# To change the payload into encoded form 
p.set_payload((attachment).read()) 

  
# encode into base64 
encoders.encode_base64(p) 
   
p.add_header('Content-Disposition', "attachment; filename= %s" % 'unfollowers.csv') 

# attach the instance 'p' to instance 'msg' 
msg.attach(p) 
  
# creates SMTP session 
s = smtplib.SMTP('smtp.gmail.com', 587) 
  
# start TLS for security 
s.starttls() 
  
# Authentication 
s.login(fromaddr, "your email password") 
  
# Converts the Multipart msg into a string 
text = msg.as_string() 
  
# sending the mail 
try:
    s.sendmail(fromaddr, email, text) 
    print('Successfully send the email to the address you mentioned above')
    print(email)
except:
    print('Sorry, the email can not be sent...')
# terminating the session 
s.quit() 