import time
from app import settings
from app import core
from datetime import datetime

def keep_track(anime, tipo):
    fecha = datetime.now()
    if tipo == 1: # Web Scraping
        archivo = 'lectura'
    elif tipo == 2: # enviado
        archivo = 'envio'
    else: # error
        tipo = 3
        archivo = 'errores'
    with open(archivo + '.csv', 'a') as f:
        texto = '{},{},{},{} \n'.format(tipo, anime.id, fecha, anime.url)
        f.write(texto)
    with open(archivo + '.dat', 'a') as f:
        texto = '{} \t\t\t {} \t\t\t {} \t\t\t {} \n'.format(tipo, anime.id, fecha, anime.url)
        f.write(texto)

def different_anime(anime, tipo=1):
    if tipo != 3:
        anime_2 = core.Anime()
        keep_track(anime_2, tipo)
        if not (anime.id == anime_2.id):
            return anime_2, True
        else:
            return anime, False
    else:
        keep_track(anime, tipo)

def main(mensaje_base, remitente, destinatario, asunto):
    anime, send = different_anime(core.Anime())
    send = True
    while True:
        try:
            anime_trys = 0
            while not (anime.id or anime.image_url or anime.name or anime.synopsis or anime.url):
                anime_trys += 1
                if anime_trys >= 3:
                    break
                anime = core.Anime()
                time.sleep(60)
            if send:
                mensaje = mensaje_base%(anime.url, anime.name, anime.image_url, anime.name, anime.synopsis)
                mail = core.Mail(mensaje, remitente, destinatario, asunto)
                mail.send_mail()
                keep_track(anime, 2)
            time.sleep(settings.WAIT)
            anime, send = different_anime(anime)
        except:
            anime, send = different_anime(anime, 3)


if __name__ == '__main__':
    main(settings.MENSAJE_BASE, settings.REMITENTE, settings.DESTINATARIO, settings.ASUNTO)

