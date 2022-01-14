import requests
from bs4 import BeautifulSoup
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
from sys import argv

now = datetime.datetime.now()

content = ''

def extract_news(url):
    print('Extracting Hacker News Stories...')
    cnt = ''
    cnt += ('<b>HN Top Stories:</b>\n'+'<br>'+'-'*50+'<br>')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content,'html.parser')
    for i,tag in enumerate(soup.find_all('td',attrs={'class':'title','valign':''})):
        cnt += ((str(i+1) + ' :: ' + tag.text + "\n" + '<br>')
            if tag.text != 'More' 
            else 
            '')
        #print(tag,prettify) #find.all('span',attrs={'class':'sitestr'}))
    return(cnt)

cnt = extract_news('https://news.ycombinator.com/')
content += cnt
content += ('<br>-----<br>')
content += ('<br><br>End of Message')

print('Composing Email...')

SERVER = 'smtp.gmail.com'
PORT = 587
TO = 'melvinhicklin@gmail.com'
FROM = 'phonefarmhicklin@gmail.com'
PASS = '3ER53q95TH&N5X88m7!d'

# fp = open(file_name, 'rb')
# msg = MIMEText('')
msg = MIMEMultipart()

#msg.add_header('Content-Disposition', 'attachemnt', filename='empty.txt')
msg['Subject'] = 'Top News Stories HN [Automated Email]' + '' + str(now.day) + '-' + str(now.month) + '-' + str(now.year)
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))
#fp.close()

print('Initiating  Server...')
server = smtplib.SMTP(SERVER, PORT)
#server = smtplib.SMTP SSL('smtp.gmail.com', 465)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
#server.ehlo
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email Sent...')

server.quit()