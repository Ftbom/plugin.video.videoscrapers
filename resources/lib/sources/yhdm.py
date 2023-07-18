import requests
import datetime
import resources.lib.fmt as fmt
from bs4 import BeautifulSoup

class Source():
    def __init__(self, url) -> None:
        self.baseUrl = url #基础链接
        #分类
        self.categroies = {
            "主页": "home",
            "热血": "66",
            "格斗": "64",
            "恋爱": "91",
            "校园": "70",
            "搞笑": "67",
            "LOLI": "111",
            "神魔": "83",
            "机战": "81",
            "科幻": "75",
            "真人": "74",
            "青春": "84",
            "魔法": "73",
            "美少女": "72",
            "神话": "102",
            "冒险": "61",
            "运动": "69",
            "竞技": "62",
            "童话": "103",
            "亲子": "63",
            "教育": "95",
            "励志": "85",
            "剧情": "77",
            "社会": "79",
            "后宫": "99",
            "战争": "80",
            "吸血鬼": "119",
            "新番动漫": str(datetime.datetime.today().year), #当年新番
            "剧场版": "37",
            "OVA版": "36",
            "真人版": "38"
        }
        self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
                'Referer' : self.baseUrl
        }
    
    #爬取主页
    def __home_parser(self) -> dict:
        url = self.baseUrl
        res = requests.get(url, headers = self.headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        categroies = []
        #主页类别
        for categroy in soup.find('div', class_ = 'firs').find_all('div', class_ = 'dtit'):
            categroies.append(categroy.h2.get_text())
        anime_lists = soup.find('div', class_ = 'firs').find_all('div', class_ = 'img')
        #结果
        results = []
        for i in range(len(anime_lists)):
            for item in anime_lists[i].find_all('li'):
                results.append({
                    'title': item.a.img.attrs['alt'],
                    'cover': item.a.img.attrs['src'],
                    'id': item.a.attrs['href'].replace('/show/', '').replace('.html', ''),
                    'description': [fmt.color(item.find_all('p')[1].get_text(), 'pink'), fmt.italics(categroies[i])]
                })
        return {'cover_headers': self.headers, 'results': results}

    def index_parser(self, id: str, page: int) -> dict:
        if (id == "home"):
            if (page == 0):
                return self.__home_parser()
            else:
                return {'cover_headers': self.headers, 'results': []}
        #获取链接
        if (page == 0):
            url = f"{self.baseUrl}/{id}/"
        else:
            url = f"{self.baseUrl}/{id}/{page + 1}.html"
        res = requests.get(url, headers = self.headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        items = soup.find('div', class_ = 'lpic').find_all('li')
        results = []
        for item in items:
            #获取描述信息
            #列表形式，每行存为一个列表元素
            spans = item.find_all('span')
            description = []
            description.append(fmt.color(spans[0].get_text(), 'pink'))
            categroies_text = []
            for i in spans[1].find_all('a'):
                categroies_text.append(i.get_text())
            description.append(fmt.italics(','.join(categroies_text)))
            description.append(fmt.lighten(item.p.get_text()))
            #结果
            results.append({
                'title': item.a.img.attrs['alt'],
                'cover': item.a.img.attrs['src'],
                'id': item.a.attrs['href'].replace('/show/', '').replace('.html', ''),
                'description': description
            })
        return {'cover_headers': self.headers, 'results': results}

    def search_parser(self, query: str, page: int) -> dict:
        url = f"{self.baseUrl}/search/{query}?page={page + 1}"
        res = requests.get(url, headers = self.headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        items = soup.find('div', class_ = 'lpic').find_all('li')
        results = []
        for item in items:
            #获取描述
            #列表形式，每行存为一个列表元素
            spans = item.find_all('span')
            description = []
            description.append(fmt.color(spans[0].get_text(), 'pink'))
            categroies_text = []
            for i in spans[1].find_all('a'):
                categroies_text.append(i.get_text())
            description.append(fmt.italics(','.join(categroies_text)))
            description.append(fmt.lighten(item.p.get_text()))
            #结果
            results.append({
                'title': item.a.img.attrs['alt'],
                'cover': item.a.img.attrs['src'],
                'id': item.a.attrs['href'].replace('/show/', '').replace('.html', ''),
                'description': description
            })
        return {'cover_headers': self.headers, 'results': results}

    def playlist_parser(self, id: str) -> dict:
        url = f"{self.baseUrl}/show/{id}.html"
        res = requests.get(url, headers = self.headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        #获取集列表
        results = []
        items = soup.find('div', class_ = "movurl").find_all('li')
        for item in items:
            results.append({
                'title': item.a.get_text(),
                'id': item.a.attrs['href'].replace('/v/', '').replace('.html', '')
            })
        #获取描述
        description = []
        description.append(fmt.color(soup.find('div', class_ = 'sinfo').p.get_text(), 'pink'))
        for i in soup.find('div', class_ = 'sinfo').find_all('span'):
            description.append(fmt.italics(i.get_text().replace('\n', ',').strip(',')))
        description.append(fmt.lighten(soup.find('div', class_ = 'info').get_text().replace('\r\n', '')))
        return {'cover': soup.find(class_ = 'thumb').img.attrs['src'], 'cover_headers': self.headers,
                'title': soup.find('div', class_ = 'rate').h1.get_text(),
                'description': description, 'results': results}

    def play_parser(self, id: str) -> list:
        url = f"{self.baseUrl}/v/{id}.html"
        res = requests.get(url, headers = self.headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        play_url = soup.find('div', id = 'playbox').attrs['data-vid'].split('$')[0]
        if not play_url.startswith('http'): #偶尔获取播放链接错误
            return []
        return [{'headers': self.headers, 'title': '播放', 'url': play_url}]