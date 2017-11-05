from bs4 import BeautifulSoup
import requests
import time
from smtplib import SMTP
from email.mime.text import MIMEText
import os

def scraping():
    url = 'www.animeflv.net'
    response = requests.get("https://" + url)
    soup = BeautifulSoup(response.content, 'html.parser')
    anime = soup.find_all('div', {'class':'AnimeDia'})
    title = anime[0].find('span', {'class': 'Title'}).string
    image_url = 'https://' + url + anime[0].find('img')['src']
    synopsis = anime[0].find('div', {'class': 'Synopsis',}).find('div', {'class': 'Description'}).string
    return title, image_url, synopsis

def send_mail(mensaje):#https://support.google.com/mail/?p=BadCredentials
    REMITENTE = "Yo <andresfelipe.2031@gmail.com>" 
    DESTINATARIO = "andresfelipe.2031@gmail.com" 
    ASUNTO = "Anime del día"

    mime_message = MIMEText(mensaje, 'html')
    mime_message["From"] = REMITENTE
    mime_message["To"] = DESTINATARIO
    mime_message["Subject"] = ASUNTO
    # Datos
    username = 'andresfelipe.2031@gmail.com'
    password = os.environ['SECRET_EMAIL_KEY']
    
    # Enviando el correo
    server = SMTP('smtp.gmail.com:587')
    server.starttls()
    server.ehlo()
    server.login(username,password)
    server.sendmail(REMITENTE, DESTINATARIO, mime_message.as_string())
    server.quit()

def main(seconds):
    
    MENSAJE_BASE = """
        <h1>El anime del dia es: <strong> %s </strong> </h1>
        <figure>
            <img src="%s" alt="%s">
        </figure>
        <h3>Sinopis: </h3>
        <p> %s </p>
        """
    while True:
        title, image_url, synopsis = scraping()
        mensaje = MENSAJE_BASE%(title, image_url, title, synopsis)
        send_mail(mensaje)
        time.sleep(seconds)

if __name__ == '__main__':
    h = 24
    m = 60
    s = 60
    main(s*m*h)
