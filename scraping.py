from bs4 import BeautifulSoup
import requests
import time
import shutil
import os
import smtplib

def scraping():
    url = 'www.animeflv.net'
    response = requests.get("https://" + url)
    soup = BeautifulSoup(response.content, 'html.parser')
    anime = soup.find_all('div', {'class':'AnimeDia'})
    title = anime[0].find('span', {'class': 'Title'}).string#find('strong')
    image_url = 'https://' + url + anime[0].find('img')['src']
    image_name = image_url.split("/")[len(image_url.split("/"))-1]
    with open(image_name, 'wb') as f:
        r = requests.get(image_url, stream=True)
        shutil.copyfileobj(r.raw, f)
    synopsis = anime[0].find('div', {'class': 'Synopsis',}).find('div', {'class': 'Description'}).string
    return title, image_url, image_name, synopsis

def main(seconds):
    REMITENTE = "<andresfelipe.2031@gmail.com>" 
    DESTINATARIO = "<andresfelipe.2031@gmail.com>" 
    ASUNTO = "Anime del día"
    MENSAJE_BASE = """
        <h1>El anime del dia es: <strong> %s </strong> </h1>
        <figure>
            <img src="%s" alt="%s">
        </figure>
        <span>sinopis: </span>
        <p> %s </p>
        """
    BASE_DIR = os.path.dirname(__file__)
    # smtp = smtplib.SMTP('localhost')
    # smtp.sendmail(REMITENTE, DESTINATARIO, mensaje)
    while True:
        title, image_url, image_name, synopsis = scraping()
        mensaje = MENSAJE_BASE%(title, image_url, title, synopsis)
        print(mensaje)
        time.sleep(seconds)


if __name__ == '__main__':
    h = 24
    m = 60
    s = 60
    main(s*m*h)
