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

def different_anime(anime):
    anime_2 = core.Anime()
    keep_track(anime_2, 1)
    if not (anime.id == anime_2.id):
        return anime_2, True
    else:
        return anime, False


def main(mensaje_base, remitente, destinatario, asunto):
    anime, send = different_anime(core.Anime())
    send = True
    while True:
        if send:
            mensaje = mensaje_base%(anime.url, anime.name, anime.image_url, anime.name, anime.synopsis)
            mail = core.Mail(mensaje, remitente, destinatario, asunto)
            mail.send_mail()
            keep_track(anime, 2)
        time.sleep(settings.WAIT)
        anime, send = different_anime(anime)


if __name__ == '__main__':
    main(settings.MENSAJE_BASE, settings.REMITENTE, settings.DESTINATARIO, settings.ASUNTO)
    