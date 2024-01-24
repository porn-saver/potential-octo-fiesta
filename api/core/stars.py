import json

from .core import *
from api.controllers.star.models.StarModel import StarModel
from ..controllers.star.config.ScrapStar import scrap
from ..controllers.star.models.DetailStarModel import DetailStarModel
from ..controllers.star.models.SortEnum import SORTENUM
from ..shared.ErrorResponse import ErrorResponse


class Stars(object):

    def __init__(self, ProxyDictionary, keywords=[], *args):
        self.keywords = keywords
        self.ProxyDictionary = ProxyDictionary

    def _sortStars(self, sort_by):
        sort_dict = dict()
        if not sort_by:
            return sort_dict

        for key in SORTENUM:
            if key.value == sort_by.lower() and key.value != "rank":
                sort_dict["o"] = key.name
                return sort_dict

        return sort_dict

    def _craftStarsPage(self, page_num, sort_by, payload=dict()):
        aux = payload.copy()
        for k in payload:
            if payload[k] == '':
                aux.pop(k)
        stars_sort = self._sortStars(sort_by)
        payload = aux
        for key in stars_sort:
            payload[key] = stars_sort[key]
        payload["page"] = page_num
        return payload

    def _loadStarsPage(self, page_num, sort_by):
        payload = dict()
        payload["search"] = ""
        minAge = '18'
        maxAge = '99'
        for item in self.keywords:
            if item[0] == 'minAge':
                minAge = item[1] if item[1].isdigit() else '18'
            if item[0] == 'maxAge':
                maxAge = item[1] if item[1].isdigit() else '99'
            elif item[0] != 'minAge' and item[0] != 'minAge' and item[0] != 'page' and item[0] != 'quantity' and item[
                0] != 'sort_by':
                payload[item[0]] = item[1]
        payload["age"] = minAge + '-' + maxAge
        r = requests.get(BASE_URL + PORNSTARS_URL, params=self._craftStarsPage(page_num, sort_by, payload),
                         headers=HEADERS,
                         proxies=self.ProxyDictionary,
                         verify=True)
        html = r.text
        return BeautifulSoup(html, "lxml")

    def _loadStarPage(self, name):
        r = requests.get(BASE_URL + PORNSTAR_URL + name,
                         headers=HEADERS,
                         proxies=self.ProxyDictionary)
        html = r.text

        return BeautifulSoup(html, "lxml")

    def _loadModelPage(self, name):
        r = requests.get(BASE_URL + MODEL_URL + name,
                         headers=HEADERS,
                         proxies=self.ProxyDictionary)
        html = r.text

        return BeautifulSoup(html, "lxml")

    def _scrapLiStar(self, soup_data):
        # get div with list of stars (month popular is the 1st)
        element = scrap["profile"][0]
        elementClass = scrap["profile"][1]
        aux = soup_data.findAll(element, class_=elementClass)
        body = soup_data.prettify()
        body = ''.join(char for char in body if char !='\n')
        body = body.replace('\&quot;','')
        body = body.replace('\"', '')

        return aux if len(aux) != 0 else {"msg": body}

    def _scrapLiStars(self, soup_data):
        # get div with list of stars (month popular is the 1st)
        aux = soup_data.findAll(scrap["listStars"][0], {"class": scrap["listStars"][1], "id": scrap["listStars"][2]})
        if len(aux) == 0:
            return {"msg": "Data no found"}
        noResults = aux[0].find_all(scrap["noResults"][0], class_=scrap["noResults"][1])
        if len(noResults) > 0:
            return {"msg": "Data no found"}
        div_el = aux[0]
        # get each porn star info (held in list block)
        li_el = div_el.find_all("li")
        if len(li_el) == 0:
            return {"msg": "Data no found"}
        return li_el

    def _scrapStarInfo(self, li_el):
        star = StarModel()
        # scrap rank
        for span_tag in li_el.find_all(scrap['listRank'][0], class_=scrap["listRank"][1]):
            try:
                star.rank = int(span_tag.text)
            except Exception as e:
                pass

        # scrap name and url
        for a_tag in li_el.find_all(scrap["listUrl"][0], href=True):
            try:
                url = a_tag.attrs["href"]
                if isStar(url):
                    star.url = BASE_URL + url
                    break
            except Exception as e:
                pass

        for span_tag in li_el.find_all(scrap["listName"][0], class_=scrap["listName"][1]):
            try:
                name = ''
                for x in span_tag.text.split():
                    name += ' ' + x
                star.name = name.strip()
                break
            except Exception as e:
                pass
        if star.name is None:
            for span_tag in li_el.find_all(scrap["listName"][0], class_=scrap["listName"][2]):
                try:
                    name = ''
                    for x in span_tag.text.split():
                        name += ' ' + x
                    star.name = name.strip()
                    break
                except Exception as e:
                    pass
        # scrap photo url
        for img_tag in li_el.find_all(scrap["listImg"][0], src=True):
            try:
                photo_url = img_tag.attrs[scrap["listImg"][1]]
                if isStarPhoto(photo_url):
                    star.photo = photo_url
                    break
            except Exception as e:
                pass

        # scrap num of videos and views
        for span_tag in li_el.find_all(scrap["listVideos"][0], class_=scrap["listVideos"][1]):
            try:
                star.videos = int(span_tag.text.split()[0])
                break
            except Exception as e:
                pass

        for span_tag in li_el.find_all(scrap["listViews"][0], class_=scrap["listViews"][1]):
            try:
                star.views = span_tag.text.split()[0]
                break
            except Exception as e:
                pass

        # scrap badges
        for span_tag in li_el.find_all(scrap["listVerified"][0], class_=scrap["listVerified"][1]):

            if span_tag.find_all(scrap["listVerified"][2], class_=scrap["listVerified"][3]):
                star.verified = True

            if span_tag.find_all(scrap["listVerified"][2], class_=scrap["listVerified"][4]):
                star.trophy = True

        # scrap type
        try:
            if "pornstar" in star.url:
                star.type = "pornstar"
            else:
                star.type = "model"
        except Exception as e:
            pass

        # return
        return star if not star.checkValues() else False

    def _scrapOneStarInfo(self, section):
        star = DetailStarModel()

        # scrap rank
        for div_tag in section.find_all(scrap["starRank"][0], class_=scrap["starRank"][1]):
            try:
                span = div_tag.find_all(scrap["starRank"][2], class_=scrap["starRank"][3])
                star.rank = int(span[0].text)
            except Exception as e:
                pass

        for h1 in section.find_all(scrap["starName"][0], itemprop=scrap["starName"][1]):
            try:
                name = ''.join(char for char in h1.text if char.isalnum() or char.isspace())
                star.name = name.strip()
                break
            except Exception as e:
                pass

        # scrap name and url
        for a_tag in section.find_all(scrap["starUrl"][0], id=scrap["starUrl"][1]):
            try:
                elementA = a_tag.find_all(scrap["starUrl"][2])
                url = elementA[0].attrs[scrap["starUrl"][3]]
                if isStar(url):
                    star.url = BASE_URL + url
                    break
            except Exception as e:
                pass

        # scrap photo url
        for img_tag in section.find_all(scrap["starPhoto"][0], id=scrap["starPhoto"][1]):
            try:
                photo_url = img_tag.attrs[scrap["starPhoto"][2]]
                if isStarPhoto(photo_url):
                    star.photo = photo_url
                    break
            except Exception as e:
                pass
        for img_tag in section.find_all(scrap["starPosterPhoto"][0], id=scrap["starPosterPhoto"][1]):
            try:
                photo_url = img_tag.attrs[scrap["starPosterPhoto"][2]]
                if isStarPhoto(photo_url):
                    star.posterPhoto = photo_url
                    break
            except Exception as e:
                pass

        for div_tag in section.find_all(scrap["starVideosViews"][0], class_=scrap["starVideosViews"][1]):
            try:
                span = div_tag.find_all(scrap["starVideosViews"][2])
                views = ''.join(char for char in span[0].text if char.isalnum() or char.isspace())
                star.views = views.strip()
                break
            except Exception as e:
                pass

        for div_tag in section.find_all(scrap["starSubs"][0], class_=scrap["starSubs"][1]):
            try:
                span = div_tag.find_all(scrap["starSubs"][2])
                subs = ''.join(char for char in span[0].text if char.isalnum() or char.isspace())
                star.subscribers = subs.strip()
                break
            except Exception as e:
                pass
        if not star.subscribers:
            for div_tag in section.find_all(scrap["starSubs"][0], class_=scrap["starSubs"][3]):
                try:
                    divs = div_tag.find_all(scrap["starSubs"][4], recursive=False)
                    value = divs[2] if len(divs) >= 3 else ''
                    if not value: pass
                    span = value.find_all(scrap["starSubs"][5])
                    subs = ''.join(char for char in span[0].text if char.isalnum() or char.isspace())
                    star.subscribers = subs.strip()
                    break
                except Exception as e:
                    pass
        # scrap badges
        for span_tag in section.find_all(scrap["starVerified"][0], class_=scrap["starVerified"][1]):

            if span_tag.find_all(scrap["starVerified"][2], class_=scrap["starVerified"][3]):
                star.verified = True

            if span_tag.find_all(scrap["starVerified"][4], class_=scrap["starVerified"][5]):
                star.trophy = True

        for div_tag in section.find_all(scrap["starBio"][0], class_=scrap["starBio"][1]):
            try:
                divs = div_tag.find_all(scrap["starBio"][2])
                bio = divs[1].text if len(divs) >= 2 else ''
                bio = ''.join(char for char in bio if char.isalnum() or char.isspace())
                star.bio = bio.strip()
            except Exception as e:
                pass

        personalInfo = dict()
        for div_tag in section.find_all(scrap["starPersonal"][0], class_=scrap["starPersonal"][1]):
            try:
                spans = div_tag.find_all(scrap["starPersonal"][2]);
                if len(spans) > 0:
                    name = self.to_camel_case(spans[0].text)
                    value = ''.join(char for char in spans[1].text if char.isalnum() or char.isspace())
                    personalInfo[name] = value.strip()
            except Exception as e:
                pass
        star.personalInfo = personalInfo
        for ul_tag in section.find_all(scrap["starSocial"][0], class_=scrap["starSocial"][1]):
            try:
                li_elements = ul_tag.find_all(scrap["starSocial"][2])
                socialMedia = dict()
                for li in li_elements:
                    a = li.find_all(scrap["starSocial"][3])[0]
                    url = a.attrs[scrap["starSocial"][4]]
                    name = self.to_camel_case(li.find_all(scrap["starSocial"][5])[0].text)
                    socialMedia[name] = url
                star.socialMedia = socialMedia
            except Exception as e:
                pass

        # scrap type
        try:
            if "pornstar" in star.url:
                star.type = "pornstar"
            else:
                star.type = "model"
        except Exception as e:
            pass
        # return
        return star if not star.checkValues() else False

    def to_camel_case(self, text):
        words = text.split()
        camel_case_words = [words[0].lower()] + [word.capitalize() for word in words[1:]]
        camel_case_text = ''.join(camel_case_words)
        return camel_case_text.replace(':', '')

    def getStars(self, quantity, page, sort_by=None, infinity=False):
        quantity = quantity if quantity >= 1 else 1
        page = page if page >= 1 else 1
        found = 0
        while True:
            for possible_star in self._scrapLiStars(self._loadStarsPage(page, sort_by)):
                if "msg" in possible_star:
                    yield {"msg": "Data no found"}
                data_dict = self._scrapStarInfo(possible_star)
                if data_dict:
                    yield data_dict

                    if not infinity:
                        found += 1
                        if found >= quantity:
                            return

            page += 1

    def getStarByName(self, name: str):
        possible_star = self._scrapLiStar(self._loadStarPage(name))
        if "msg" in possible_star:
            possible_star = self._scrapLiStar(self._loadModelPage(name))
            if "msg" in possible_star:
                response = ErrorResponse(404, possible_star['msg'])
                yield response
            else:
                data_dict = self._scrapOneStarInfo(possible_star[0])
                if data_dict:
                    yield data_dict

    def changeStarKeyWords(self, keyWords=None):
        if keyWords is None:
            keyWords = []
        self.keywords = keyWords
