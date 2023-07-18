import sys
import xbmcplugin
import requests
from urllib.parse import urlencode

__handle__ = int(sys.argv[1])

headless_api_keys = {
    'scrapingant': xbmcplugin.getSetting(__handle__, 'scrapingant'),
    'scrapingbee': xbmcplugin.getSetting(__handle__, 'scrapingbee'),
    'zenscrape': xbmcplugin.getSetting(__handle__, 'zenscrape'),
    'scraperapi': xbmcplugin.getSetting(__handle__, 'scraperapi')
}

api_select = xbmcplugin.getSetting(__handle__, 'api-select')

def get_by_scrapingant(url: str):
    data = {'url': url, 'x-api-key': headless_api_keys['scrapingant']}
    url = f"https://api.scrapingant.com/v2/general?{urlencode(data)}"
    res =  requests.get(url)
    return res.text

def get_by_scrapingbee(url: str):
    res = requests.get(
        url='https://app.scrapingbee.com/api/v1/',
        params={
            'api_key': headless_api_keys['scrapingbee'],
            'url': url,  
        }
    )
    return res.text

def get_by_zenscrape(url: str):
    headers = { 
        "apikey": headless_api_keys['zenscrape']
    }
    params = (
        ("url", url),
        ("render", "true"),
    )
    res = requests.get('https://app.zenscrape.com/api/v1/get', headers=headers, params=params)
    return res.text

def get_by_scraperapi(url: str):
    res = requests.get(f'http://api.scraperapi.com?api_key={headless_api_keys["scraperapi"]}&url={url}&render=true')
    return res.text

headless_api_funcs = {
    'scrapingant': get_by_scrapingant,
    'scrapingbee': get_by_scrapingbee,
    'zenscrape': get_by_zenscrape,
    'scraperapi': get_by_scraperapi
}

def get_html_text(url: str):
    func = headless_api_funcs[api_select]
    return func(url)
