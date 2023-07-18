import json
import base64
import requests

class Source():
    def __init__(self, url: str) -> None:
        self.baseUrl = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Referer' : self.baseUrl
        }
        self.categroies = {}

    def index_parser(self, id: str, page: int) -> dict:
        return {'cover_headers': {}, 'results': []}
    
    def search_parser(self, query: str, page: int) -> dict:
        if (page > 0):
            return {'cover_headers': {}, 'results': []} 
        url = f"{self.baseUrl}/api.php?tp=jsonp&wd={query}"
        res = requests.get(url, headers = self.headers).json()
        results = []
        for i in res['info']:
            description = [f"类型：{i['type']}", f"来源：{i['from']}"]
            if i['img:'] == 'null':
                cover = ''
            else:
                cover = i['img:']
            results.append({
                "title": i['title'],
                "cover": cover,
                "id": f"{i['flag']}_{i['id']}",
                "description": description
            })
        return {'cover_headers': self.headers, 'results': results}
    
    def playlist_parser(self, id: str) -> dict:
        params = id.split('_')
        url = f"{self.baseUrl}/api.php?out=jsonp&flag={params[0]}&id={params[1]}"
        res = requests.get(url, headers = self.headers)
        data = json.loads(res.text[1: -2])
        results = []
        for i in data['info'][0]['video']:
            video_info = i.split('$')
            results.append({'title': video_info[0], 'id': base64.b64encode(video_info[1].encode('utf-8')).decode('utf-8')})
        return {'cover': data['pic'], 'cover_headers': self.headers, 'title': data['title'], 'description': [f"来源：{data['info'][0]['flag_name']}"], 'results': results}
    
    def play_parser(self, id: str) -> list:
        url = base64.b64decode(id.encode('utf-8')).decode('utf-8')
        return [{'headers': self.headers, 'title': '播放', 'url': url}]
