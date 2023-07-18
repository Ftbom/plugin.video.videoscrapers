import json
import requests
import datetime
from urllib.parse import quote
from bs4 import BeautifulSoup
import resources.lib.fmt as fmt

class Source():
    def __init__(self, url: str) -> None:
        self.baseUrl = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Referer' : self.baseUrl
        }
        self.categroies = {
            "首页": "home",
            f"{str(datetime.datetime.today().year)}热播": f"{str(datetime.datetime.today().year)}meijutop",
            "魔幻科幻": "list1",
            "灵异惊悚": "list2",
            "都市情感": "list3",
            "犯罪历史": "list4",
            "选秀综艺": "list5",
            "动漫卡通": "list6"
        }
    
    def __home_parser(self) -> dict:
        url = self.baseUrl
        res = requests.get(url, headers = self.headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        results = []
        for items in soup.find_all('div', class_ = "cn3_r"):
            categroy = items.find('div', class_ = 'Title').b.get_text()
            for item in items.find('div', class_ = "c2_contact").find_all('li'):
                results.append({
                    'title': item.a.img.attrs['alt'],
                    'cover': item.a.img.attrs['src'],
                    'id': item.a.attrs['href'].replace('/content/', '').replace('.html', ''),
                    'description': [fmt.color(item.find_all('p')[1].get_text(), 'orange'), fmt.italics(categroy)]
                })
        for items in soup.find_all('div', class_ = "cn3_l"):
            categroy = items.find('div', class_ = 'Title').b.get_text()
            for item in items.find('div', class_ = "c2_contact").find_all('li'):
                results.append({
                    'title': item.a.img.attrs['alt'],
                    'cover': item.a.img.attrs['src'],
                    'id': item.a.attrs['href'].replace('/content/', '').replace('.html', ''),
                    'description': [fmt.color(item.find_all('p')[1].get_text(), 'orange'), fmt.italics(categroy)]
                })
        return {'cover_headers': self.headers, 'results': results}
    
    def __top_parser(self, id: str) -> dict:
        url = self.baseUrl + f"/{id}.html"
        res = requests.get(url, headers = self.headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        results = []
        for item in soup.find_all("div", class_ = "self_box"):
            description = []
            for info in item.find("ul", class_ = "self_con").find_all("li"):
                description.append(info.get_text())
            description[0] = fmt.italics(description[0])
            description[1] = fmt.color(description[1], "orange")
            other_info = item.find("div", class_ = "self_img")
            results.append({
                "title": other_info.a.img.attrs['alt'],
                "cover": other_info.a.img.attrs['src'],
                "id": other_info.a.attrs['href'].replace('/content/', '').replace('.html', ''),
                "description": description
            })
        return {'cover_headers': self.headers, 'results': results}
    
    def index_parser(self, id: str, page: int) -> dict:
        if (id == "home"):
            if (page == 0):
                return self.__home_parser()
            else:
                return {'cover_headers': self.headers, 'results': []}
        if ("list" in id):
            id = f"/file/{id}"
        else:
            if (page == 0):
                return self.__top_parser(id)
            else:
                return {'cover_headers': self.headers, 'results': []}
        if (page == 0):
            url = self.baseUrl + id + ".html"
        else:
            url = self.baseUrl + f"{id}_{page + 1}.html"
        res = requests.get(url, headers = self.headers)
        if "404 Error" in str(res.content): #无内容
            return {'cover_headers': self.headers, 'results': []}
        soup = BeautifulSoup(res.content, 'html.parser')
        results = []
        for item in soup.find_all("div", class_ = "cn_box2"):
            description = []
            for info in item.find("ul", class_ = "list_20").find_all("li"):
                description.append(info.get_text())
            description[0] = fmt.italics(description[0])
            description[1] = fmt.color(description[1], "orange")
            other_info = item.find("div", class_ = "bor_img3_right")
            results.append({
                "title": other_info.a.img.attrs['alt'],
                "cover": other_info.a.img.attrs['src'],
                "id": other_info.a.attrs['href'].replace('/content/', '').replace('.html', ''),
                "description": description
            })
        return {'cover_headers': self.headers, 'results': results}
    
    def search_parser(self, query: str, page: int) -> dict:
        url = f"{self.baseUrl}/sousuo/index.asp?page={page + 1}&searchword={quote(query.encode('gbk'))}&searchtype=-1"
        res = requests.get(url, headers = self.headers)
        if "404 Error" in str(res.content): #无内容
            return {'cover_headers': self.headers, 'results': []}
        soup = BeautifulSoup(res.content, 'html.parser')
        results = []
        for item in soup.find_all("div", class_ = "cn_box2"):
            description = []
            for info in item.find("ul", class_ = "list_20").find_all("li"):
                description.append(info.get_text())
            description[0] = fmt.italics(description[0])
            description[1] = fmt.color(description[1], "orange")
            other_info = item.find("div", class_ = "bor_img3_right")
            results.append({
                "title": other_info.a.img.attrs['alt'],
                "cover": other_info.a.img.attrs['src'],
                "id": other_info.a.attrs['href'].replace('/content/', '').replace('.html', ''),
                "description": description
            })
        return {'cover_headers': self.headers, 'results': results}
    
    def playlist_parser(self, id: str) -> dict:
        url = f"{self.baseUrl}/content/{id}.html"
        res = requests.get(url, headers = self.headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        cover = soup.find('div', class_ = "o_big_img_bg_b").img.attrs['src']
        title = soup.find('div', class_ = "info-title")
        title = title.span.get_text() + title.h1.get_text()
        description = []
        for info in soup.find('div', class_ = 'o_r_contact').find_all('li'):
            description.append(info.get_text())
        description[0] = fmt.color(description[0], 'orange')
        results = []
        for item in soup.find('ul', class_ = 'mn_list_li_movie').find_all('li'):
            results.append({
                'title': item.a.attrs['title'],
                'id': item.a.attrs['href'].replace('/video/', '').replace('.html', '')
            })
        return {'cover': cover, 'cover_headers': self.headers,
                'title': title, 'description': description, 'results': results}
    
    def play_parser(self, id: str) -> list:
        num = int(id.split('-')[-1])
        url = f"{self.baseUrl}/video/{id}.html"
        res = requests.get(url, headers = self.headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        for script in soup.find_all('script'):
            if not 'src' in script.attrs:
                continue
            if 'playdata' in script.attrs['src']:
                res = requests.get(self.baseUrl + script.attrs['src'], headers = self.headers)
                start = res.text.find('var VideoListJson=')
                end = res.text.find(',urlinfo=')
                datas = json.loads(res.text[start + 18 : end])
        results = []      
        for data in datas:
            if '云播' in data[0]:
                url = data[1][num][1]
                url = url[0 : url.find('index') + 5] + '.m3u8'
                results.append({'headers': self.headers, 'title': data[0], 'url': url})
        return results
