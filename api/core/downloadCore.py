import asyncio

from fastapi import WebSocket

import yt_dlp
import requests
import urllib.parse as urlparse

from api.controllers.socket.ConnectionManager import ConnectionManager

downloadManager: ConnectionManager = None
downloadSocket: WebSocket = None


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


async def custom_dl_download(url, manager: ConnectionManager, socket: WebSocket):
    # ph_url_check(url)
    ph_alive_check(url)

    global downloadManager
    global downloadSocket
    downloadManager = manager
    downloadSocket = socket

    outtmpl = './api/downloads/%(title)s.%(ext)s'
    ydl_opts = {
        'format': 'best',
        'outtmpl': outtmpl,
        'nooverwrites': True,
        'no_warnings': False,
        'ignoreerrors': True,
        'n_threads': 100,
        'geo_bypass': True,
        'progress_hooks': [progress_hook],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        await asyncio.to_thread(ydl.download, [url])


def progress_hook(d):
    if d['status'] == 'finished':
        print('Descarga completa!')
        data = {'status': 'finish', 'percent': '100%', 'speed': 0}
        asyncio.run(sendJson(data))
        return
    elif d['status'] == 'downloading':
        percent = d['_percent_str']
        speed = d['_speed_str']
        data = {'status': 'downloading', 'percent': percent, 'speed': speed}
        asyncio.run(sendJson(data))


async def sendJson(data):
    global downloadManager
    global downloadSocket
    await downloadManager.send_json(data, downloadSocket)


async def finishSocket():
    global downloadManager
    global downloadSocket
    await downloadManager.disconnect(downloadSocket)
