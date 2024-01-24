import socket

import youtube_dl
import requests
import urllib.parse as urlparse


def initSocket():
    return

def my_hook(d):
    if d['status'] == 'finished':
        print('Descarga completa!')
        # Puedes enviar los datos a través del socket aquí

    if d['status'] == 'downloading':
        percent = d['_percent_str']
        speed = d['_speed_str']
        print(f'{percent} - {speed}', end='\r')
        # Puedes enviar los datos a través del socket aquí


def ph_url_check(url):
    parsed = urlparse.urlparse(url)
    regions = ["www", "cn", "cz", "de", "es", "fr", "it", "nl", "jp", "pt", "pl", "rt"]
    for region in regions:
        if parsed.netloc == region + ".pornhub.com":
            print("PornHub url validated.")
            return
    print("This is not a PornHub url.")


def ph_alive_check(url):
    requested = requests.get(url)
    if requested.status_code == 200:
        print("and the URL is existing.")
    else:
        print("but the URL does not exist.")


def custom_dl_download(url):
    # ph_url_check(url)
    ph_alive_check(url)

    outtmpl = './api/downloads/%(title)s.%(ext)s'
    ydl_opts = {
        'format': 'best',
        'outtmpl': outtmpl,
        'nooverwrites': True,
        'no_warnings': False,
        'ignoreerrors': True
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
