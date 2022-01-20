import requests

from bs4 import BeautifulSoup 
# for web-scraping
#Send the email
import smtplib
#email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#system date and time manipulation
import datetime

now = datetime.datetime.now()

#email content placeholder
content =''                             #content is global object

#Extracting Hacker News Stories
def extract_news(url):
    print('Extracting Hacker News Stories...')
    cnt = ''
    cnt += ('<b>HN Top Stories: </b>\n' + '<br>'+'-'*50+'<br>')
    response = requests.get(url)
    content = response.content          #content is local object
    
    soup = BeautifulSoup(content, 'html.parser') #using html parser to extract from local content

    #Starting for loop, extracting tag's value, enumerate for numbering
    for i, tag in enumerate(soup.find_all('td', attrs={'class':'title',  'valign':''})): cnt += ((str(i+1)+' :: '+tag.text + "\n" + '<br>') if tag.text!='More' else '')

    return(cnt)

cnt = extract_news('https://news.ycombinator.com/') #global object
content += cnt
content += ('<br>--------</br>')
content += ('<br><br>End of Message')

#Lets send the Email
print('Composing Email...')

#Update your Email details
SERVER = 'smtp.gmail.com' #Your smtp server
PORT = 587 #Your port number
FROM = ''
TO = ''
PASS = ''


#Create message body
msg = MIMEMultipart()
#Creating a dynamic Subject line
msg['Subject'] = 'Top News Stories HN [Automated Email]' + '  ' + str(now.day) + '-' + str(now.month)+ '-' + str(now.year) 
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content,'html'))

#Authentication Section
print('Initiating Server...')

server = smtplib.SMTP(SERVER, PORT) #Call smtp function
server.set_debuglevel(1) #Set value to 1 if want to see error messages
server.ehlo()
server.starttls()
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email Sent...')

server.quit()




