from bs4 import BeautifulSoup
import requests
from smtplib import SMTP
from email.mime.text import MIMEText
import os

class Anime():
    def __init__(self):
        url = 'www.animeflv.net'
        response = requests.get("https://" + url)
        soup = BeautifulSoup(response.content, 'html.parser')
        anime_div = soup.find('div', {'class':'AnimeDia'})
        title = anime_div.find('span', {'class': 'Title'}).string
        anime_url = 'https://' + url + anime_div.find('div', {'class': 'Image'}).find('a')['href']
        image_url = 'https://' + url + anime_div.find('img')['src']
        anime_id = anime_div.find('div', {'class': 'Image'}).find('a')['href']
        synopsis = anime_div.find('div', {'class': 'Synopsis',}).find('div', {'class': 'Description'}).string

        self.id = int(anime_id.split("/")[2])
        self.name = title
        self.url = anime_url
        self.image_url = image_url
        self.synopsis = synopsis

class Mail():
    def __init__(self, mensaje, remitente, destinatario, asunto):
        self.mensaje = mensaje
        self.remitente = remitente
        self.destinatario = destinatario
        self.asunto = asunto
        
    def send_mail(self):
        mime_message = MIMEText(self.mensaje, 'html')
        mime_message["From"] = self.remitente
        mime_message["To"] = self.destinatario
        mime_message["Subject"] = self.asunto

        # Datos
        username = self.remitente
        password = os.environ['SECRET_EMAIL_KEY']
        
        # Enviando el correo
        server = SMTP('smtp.gmail.com:587')
        server.starttls()
        server.ehlo()
        server.login(username,password)
        server.sendmail(REMITENTE, DESTINATARIO, mime_message.as_string())
        server.quit()

