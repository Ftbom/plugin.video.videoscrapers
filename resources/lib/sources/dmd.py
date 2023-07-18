import re
import requests
from urllib.parse import unquote
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
            '首页': 'home',
            '新番连载': '1',
            '完结日漫': '3',
            '热门国漫': '4',
            '剧场动漫': '16',
            '热血': 'vod-list-id-3-order--by--class-37-pg',
            '后宫': 'vod-list-id-3-order--by--class-41-pg',
            '奇幻': 'vod-list-id-3-order--by--class-38-pg',
            '校园': 'vod-list-id-3-order--by--class-40-pg',
            '恋爱': 'vod-list-id-3-order--by--class-39-pg',
            '神魔': 'vod-list-id-3-order--by--class-44-pg',
            '冒险': 'vod-list-id-3-order--by--class-36-pg',
            '竞技': 'vod-list-id-3-order--by--class-49-pg',
            '搞笑': 'vod-list-id-3-order--by--class-42-pg',
            '魔法': 'vod-list-id-3-order--by--class-45-pg',
            '百合': 'vod-list-id-3-order--by--class-46-pg',
        }

    def __home_parser(self):
        url = self.baseUrl
        res = requests.get(url, headers = self.headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        results = []
        top_info = soup.find('div', class_ = 'cn2_l')
        categroy = top_info.find('div', class_ = 'Title').get_text()
        for item in top_info.find('div', class_ = 'c1_l_wap_contact').find_all('li'):
            description = [fmt.italics(categroy)]
            for info in item.find_all('p', class_ = 'time'):
                description.append(info.get_text())
            description[1] = fmt.color(description[1], 'pink')
            results.append({
                'title': item.a.img.attrs['alt'],
                'cover': item.a.img.attrs['src'],
                'id': item.a.attrs['href'].replace('/detail/', '').replace('.html', ''),
                'description': description
            })
        for items in soup.find_all('div', class_ = 'cn3_l'):
            categroy = items.find('div', class_ = 'Title').b.get_text()
            for item in items.find('div', class_ = 'c1_3_wap_contact').find_all('li'):
                description = [fmt.italics(categroy)]
                for info in item.find_all('p', class_ = 'time'):
                    description.append(info.get_text())
                description[1] = fmt.color(description[1], 'pink')
                results.append({
                    'title': item.a.img.attrs['alt'],
                    'cover': item.a.img.attrs['src'],
                    'id': item.a.attrs['href'].replace('/detail/', '').replace('.html', ''),
                    'description': description
                })
        return {'cover_headers': self.headers, 'results': results}
    
    def index_parser(self, id: str, page: int) -> dict:
        if (id == 'home'):
            if (page == 0):
                return self.__home_parser()
            else:
                return {'cover_headers': self.headers, 'results': []}
        if ('vod' == id[0 : 3]):
            url = f"{self.baseUrl}/{id}-{page + 1}.html"
        else:
            url = f"{self.baseUrl}/type/{id}-{page + 1}.html"
        res = requests.get(url, headers = self.headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        results = []
        for item in soup.find_all('div', class_ = 'cn_box2'):
            info1 = item.find('div', class_ = 'bor_img3_right')
            description = []
            i = 0
            for info2 in item.find('ul', class_ = 'list_20').find_all('li'):
                if (i == 0):
                    i = i + 1
                    continue
                if (i == 1):
                    i = i + 1
                    description.append(fmt.color(info2.get_text(), 'pink'))
                    continue
                description.append(info2.get_text())
            results.append({
                'title': info1.a.img.attrs['alt'],
                'cover': info1.a.img.attrs['src'],
                'id': info1.a.attrs['href'].replace('/detail/', '').replace('.html', ''),
                'description': description
            })
        return {'cover_headers': self.headers, 'results': results}
    
    def search_parser(self, query: str, page: int) -> dict:
        url = f"{self.baseUrl}/search-pg-{page + 1}-wd-{query}.html"
        res = requests.get(url, headers = self.headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        results = []
        for item in soup.find_all('div', class_ = 'cn_box2'):
            info1 = item.find('div', class_ = 'bor_img3_right')
            description = []
            i = 0
            for info2 in item.find('ul', class_ = 'list_20').find_all('li'):
                if (i == 0):
                    i = i + 1
                    continue
                if (i == 1):
                    i = i + 1
                    description.append(fmt.color(info2.get_text(), 'pink'))
                    continue
                description.append(info2.get_text())
            results.append({
                'title': info1.a.img.attrs['alt'],
                'cover': info1.a.img.attrs['src'],
                'id': info1.a.attrs['href'].replace('/detail/', '').replace('.html', ''),
                'description': description
            })
        return {'cover_headers': self.headers, 'results': results}
    
    def playlist_parser(self, id: str) -> dict:
        url = f"{self.baseUrl}/detail/{id}.html"
        res = requests.get(url, headers = self.headers)
        soup = BeautifulSoup(res.content, 'html.parser')
        results = []
        for item in soup.find('ul', class_ = 'mn_list_li_movie').find_all('li'):
            results.append({
                'title': item.a.get_text(),
                'id': item.a.attrs['href'].replace('/play/', '').replace('.html', '')
            })
        description = []
        for item in soup.find('div', class_ = 'o_r_contact').find_all('li'):
            description.append(item.get_text())
        description[-1] = fmt.color(description[-1], 'blue')
        description[-2] = fmt.color(description[-2], 'pink')
        description[-1] = description[-1].replace('\xa0', ',')
        return {'cover': soup.find(class_ = 'o_big_img_bg_b').img.attrs['src'], 'cover_headers': self.headers,
                'title': soup.find('div', class_ = 'info-title').h1.get_text(),
                'description': description, 'results': results}
    
    def play_parser(self, id: str) -> list:
        num = int(id.split('-')[-1])
        url = f"{self.baseUrl}/play/{id}.html"
        res = requests.get(url, headers = self.headers)
        text = res.text
        start = text.find("mac_url=unescape('")
        end = text.find(".m3u8');")
        data_str = text[start + 18 : end + 5]
        data_str = unquote(re.sub(r'%u([a-fA-F0-9]{4}|[a-fA-F0-9]{2})', lambda m: chr(int(m.group(1), 16)), data_str))
        results = []
        strs = data_str.split('$$$')
        i = 1
        for str_ in strs:
            if (num < 10):
                num_str1 = '0' + str(num)
            else:
                num_str1 = str(num)
            if (num < 9):
                num_str2 = '0' + str(num + 1)
            else:
                num_str2 = str(num + 1)
            start = str_.find(f'第{num_str1}集$')
            end = str_.find(f'第{num_str2}集')
            results.append({'headers': self.headers, 'title': f'云播{i}', 'url': str_[start + len(num_str1) + 3 : end - 1]})
            i = i + 1
        return results