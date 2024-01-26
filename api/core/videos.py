# -*- coding: UTF-8 -*-

from .core import *
import re
import json

from ..controllers.video.models.SortEnum import SORTENUM
from ..controllers.video.models.VideoDetailModel import VideoDetailModel
from ..controllers.video.models.VideoModel import VideoModel


class Videos(object):

    def __init__(self, ProxyDictionary, keywords=[], *args):
        self.keywords = keywords
        self.ProxyDictionary = ProxyDictionary

    def _sortVideos(self, sort_by):
        sort_dict = dict()

        if not sort_by:
            return sort_dict

        for key in SORTENUM:
            if key.value == sort_by.lower() and key.value != "recent":
                sort_dict["o"] = key.name
                return sort_dict

        return sort_dict

    def _craftVideosURL(self, page_num, sort_by, payload=dict()):
        aux = payload.copy()
        for k in payload:
            if payload[k] == '':
                aux.pop(k)
        video_sort = self._sortVideos(sort_by)
        payload = aux
        for key in video_sort:
            payload[key] = video_sort[key]
        payload["page"] = page_num
        return payload

    def _loadPage(self, page_num=None, sort_by=None, url=None, viewkey=None):
        payload = dict()
        # load search page
        if page_num:
            search_url = BASE_URL + VIDEOS_URL
            for item in self.keywords:
                if item[0] == 'min_duration' or item[0] == 'max_duration':
                    payload[item[0]] = item[1] if item[1] != 0 else ''
                elif item[0] == 'isHd':
                    payload['hd'] = '1' if item[1] == True else ''
                elif item[0] == 'production':
                    payload['p'] = item[1]
                elif item[0] != 'min_duration' and item[0] != 'max_duration' and item[0] != 'page' and item[
                    0] != 'quantity' and \
                        item[
                            0] != 'sort_by' and item[0] != 'isHd':
                    payload[item[0]] = item[1]
            if self.keywords:
                search_url += SEARCH_URL
            r = requests.get(search_url, params=self._craftVideosURL(page_num, sort_by, payload), headers=HEADERS,
                             proxies=self.ProxyDictionary)
        else:
            if url and isVideo(url):
                r = requests.get(url, headers=HEADERS, proxies=self.ProxyDictionary)
            else:
                r = requests.get(BASE_URL + VIDEO_URL + viewkey, headers=HEADERS, proxies=self.ProxyDictionary)

        html = r.text

        return BeautifulSoup(html, "lxml")

    def _scrapLiVideos(self, soup_data):
        return soup_data.find("div", class_="sectionWrapper").find_all("li",
                                                                       {"class": re.compile(".*videoblock videoBox.*")})

    def _scrapVideosInfo(self, div_el):
        data = VideoModel()

        # scrap url, name
        for a_tag in div_el.find_all("a", href=True):
            try:
                url = a_tag.attrs["href"]
                if isVideo(url):
                    data.url = BASE_URL + url
                    data.title = a_tag.attrs["title"]
                    break
            except Exception as e:
                pass

        # scrap background photo url
        for img_tag in div_el.find_all("img", src=True):
            try:
                url = img_tag.attrs["data-mediumthumb"]
                if isVideoPhoto(url):
                    data.imageUrl = url
                    break
            except Exception as e:
                pass

        # scrap duration
        for var_tag in div_el.find_all("var", {"class": "duration"}):
            try:
                data.duration = str(var_tag).split(">")[-2].split("<")[-2]
                break
            except Exception as e:
                pass

        # scrap rating
        for div_tag in div_el.find_all("div", {"class": "value"}):
            try:
                data.rating = int(str(div_tag).split(">")[1].split("%")[0])
                break
            except Exception as e:
                pass

        for span_tag in div_el.find_all("span", {"class": "views"}):
            try:
                data.views = span_tag.text.split(" ")[0]
                break
            except Exception as e:
                pass

        for div_tag in div_el.find_all("div", class_="videoUploaderBlock"):
            try:
                values = dict()
                userValue = div_tag.find_all("a")
                values["user"] = userValue[0].text
                values["url"] = userValue[0].attrs["href"]
                values["type"] = userValue[0].attrs["href"].split('/')[1]
                data.userUploadedData = values
                break
            except Exception as e:
                pass

        return data if not data.checkValues() else False

    # Scrap duration, upload_date, author, embed_url, accurate_views
    def _scrapScriptInfo(self, soup_data, data: VideoDetailModel):
        script_dict = json.loads(soup_data.replace("'", '"'))
        data.author = script_dict["author"]
        data.duration = ":".join(re.findall(r"\d\d", script_dict["duration"]))
        data.upload_date = re.findall(r"\d{4}-\d{2}-\d{2}", script_dict["uploadDate"])[0]
        data.accurate_views = int(script_dict["interactionStatistic"][0]["userInteractionCount"].replace(",", ""))
        return data

    def _scrapVideoInfo(self, soup_data):
        data: VideoDetailModel = VideoDetailModel()
        try:
            self._scrapScriptInfo(soup_data.find("script", type="application/ld+json").text, data)
        except:
            data.title = "***Video not available in your country***"
            return data

        data.title = soup_data.find("head").find("title").text
        data.url = soup_data.find("head").find("link", rel="canonical")["href"]
        data.img_url = soup_data.find("head").find("link", rel="preload")["href"]

        video = soup_data.find("div", class_="video-wrapper")

        data.views = video.find("span", class_="count").text
        data.rating = int(video.find("span", class_="percent").text.replace("%", ""))
        data.loaded = video.find("span", class_="white").text
        data.likes = video.find("span", class_="votesUp").text
        data.accurate_likes = video.find("span", class_="votesUp")["data-rating"]
        data.dislikes = video.find("span", class_="votesDown").text
        data.accurate_dislikes = video.find("span", class_="votesDown")["data-rating"]
        data.favorite = video.find("span", class_="favoritesCounter").text.strip()
        data.production = video.find("div", class_="productionWrapper").find_all("a", class_="item")[0].text

        # Scrap pornstars
        pornstars = []
        for star in video.find_all("a", class_="pstar-list-btn"):
            s = dict()
            s["name"] = star.text.strip()
            s["url"] = star.attrs["href"]
            s["imageUrl"] = star.find_all("img")[0].attrs["src"]
            pornstars.append(s)
        data.pornstars = pornstars

        # Scrap categories
        categories = []
        for category in video.find("div", class_="categoriesWrapper").find_all("a", class_="item"):
            categories.append(category.text)
        data.categories = categories

        # Scrap tags
        tags = []
        for tag in video.find("div", class_="tagsWrapper").find_all("a", class_="item"):
            tags.append(tag.text)
        data.tags = tags
        return data

    def getVideo(self, url=None, viewkey=None, *args):
        if url or viewkey:
            return self._scrapVideoInfo(self._loadPage(url=url, viewkey=viewkey))

    def getVideos(self, quantity=1, page=1, sort_by=None, full_data=True, infinity=False):
        quantity = quantity if quantity >= 1 else 1
        page = page if page >= 1 else 1
        found = 0

        while True:
            for possible_video in self._scrapLiVideos(self._loadPage(page_num=page, sort_by=sort_by)):
                data_dict = self._scrapVideosInfo(possible_video)
                if data_dict:
                    if full_data:
                        yield self.getVideo(data_dict.url)
                    else:
                        yield data_dict

                    if not infinity:
                        found += 1
                        if found >= quantity: return

            page += 1

    def changeVideoKeyWords(self, keyWords=None):
        if keyWords is None:
            keyWords = []
        self.keywords = keyWords
