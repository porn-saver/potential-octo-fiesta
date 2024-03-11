import yt_dlp
import requests
import urllib.parse as urlparse
import os

from api.controllers.video.models.DownloadVideoModel import DownloadVideoModel


def ph_url_check(url):
    parsed = urlparse.urlparse(url)

    regions = ["www", "cn", "cz", "de", "es", "fr", "it", "nl", "jp", "pt", "pl", "rt"]
    for region in regions:
        if parsed.netloc == region + ".pornhub.com":
            return


def ph_alive_check(url):
    requested = requests.get(url)
    if requested.status_code == 200:
        print("and the URL is existing.")
    else:
        print("but the URL does not exist.")


def custom_dl_download(url):
    outtmpl = './api/downloads/%(title)s.%(ext)s'
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'outtmpl': outtmpl,
        'nooverwrites': True,
        'no_warnings': False,
        'ignoreerrors': True,
        'n_threads': 100,
        'geo_bypass': True,
        'cookiefile':'api/shared/cookies.txt'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        downloadUrls = []
        print(info)
#         for format in info['formats']:
#             if "hls" not in format["format_id"]:
#                 videoFormat: DownloadVideoModel = DownloadVideoModel()
#                 videoFormat.height = format["height"]
#                 videoFormat.resolution = format["resolution"]
#                 videoFormat.ext = format["ext"]
#                 videoFormat.format = format["format"]
#                 videoFormat.aspectRatio = format["aspect_ratio"]
#                 videoFormat.url = format["url"]
#                 downloadUrls.append(videoFormat)
        return downloadUrls
