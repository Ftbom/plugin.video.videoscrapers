import sys

import xbmc
import xbmcaddon
import xbmcplugin
import xbmcgui

import os
import json
import sqlite3
import base64
from urllib.parse import parse_qsl, quote, unquote

import resources.lib.fmt as fmt

#插件信息
__url__ = sys.argv[0]
__handle__ = int(sys.argv[1])

xbmcplugin.setContent(__handle__, 'movies')

from resources.lib.sources import video_sources

#主界面
#列出源
def mainMenu():
    menuItems = []
    #收藏
    item = xbmcgui.ListItem(label = fmt.bold(fmt.color("收藏", "red")))
    url = f'{__url__}?action=list_favorite' #action url
    menuItems.append((url, item, True))
    for member in video_sources.keys():
        if not (video_sources[member]['enable'] == 'true'): #是否启用源
            continue
        item = xbmcgui.ListItem(label = fmt.bold(fmt.color(video_sources[member]['name'], video_sources[member]['color'])))
        url = f'{__url__}?action=list_indexs&source={member}' #action url
        menuItems.append((url, item, True))
    xbmcplugin.addDirectoryItems(__handle__, menuItems, len(menuItems)) #添加条目
    xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_NONE) #不排序
    xbmcplugin.endOfDirectory(__handle__) #添加结束

#列出index列表
def list_indexs(source_name: str):
    if not (video_sources[source_name]['enable'] == 'true'):
        mainMenu()
        return
    #导入源
    module = __import__(f'resources.lib.sources.{source_name}', fromlist=[''])
    current_source = module.Source(video_sources[source_name]['url'])
    menuItems = []
    #搜索项
    menuItem = xbmcgui.ListItem (label = fmt.color('搜索', 'yellow'))
    url = f"{__url__}?action=list_search_results&source={source_name}&page=0"
    menuItems.append((url, menuItem, True))
    #类别
    for key in current_source.categroies.keys():
        menuItem = xbmcgui.ListItem (label = str(key))
        url = f"{__url__}?action=list_videos&source={source_name}&id={current_source.categroies[key]}&page=0"
        menuItems.append((url, menuItem, True))
    xbmcplugin.addDirectoryItems(__handle__, menuItems, len(menuItems))
    xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_NONE) #不排序
    xbmcplugin.endOfDirectory (__handle__)

#列出index视频列表
def list_videos(source_name: str, id: str, page: int):
    if not (video_sources[source_name]['enable'] == 'true'):
        mainMenu()
        return
    module = __import__(f'resources.lib.sources.{source_name}', fromlist=[''])
    current_source = module.Source(video_sources[source_name]['url'])
    results = current_source.index_parser(id, page) #获取列表
    menuItems = []
    #获取图片headers
    headers_str = '|'
    for header_key in results['cover_headers']:
        headers_str = headers_str + f'{header_key}={results["cover_headers"][header_key]}&'
    if (headers_str == '|'):
        headers_str == ''
    else:
        headers_str.strip('&')
    #添加结果
    for result in results['results']:
        url = f"{__url__}?action=list_plays&source={source_name}&id={result['id']}"
        menuItem = xbmcgui.ListItem(label = str(result['title']))
        cover_url = result['cover'] + headers_str
        menuItem.setArt({'poster': cover_url})
        menuItem.setInfo('video', {'plot': fmt.newline.join(result['description'])}) #显示详情
        #添加到收藏菜单
        favorite_data = {'title': str(result['title']), 'cover': cover_url, 'description': fmt.newline.join(result['description']), 'url': url}
        favorite_url = f"{__url__}?action=add_favorite&data={base64.b64encode(json.dumps(favorite_data).encode('utf-8')).decode('utf-8')}"
        menuItem.addContextMenuItems([("添加到收藏", f'RunPlugin({favorite_url})')])
        menuItems.append((url, menuItem, True))
    #下一页
    if len(results['results']) > 0:
        menuItem = xbmcgui.ListItem (label = fmt.color('>>下一页', 'yellow'))
        url = f"{__url__}?action=list_videos&source={source_name}&id={id}&page={page + 1}"
        menuItems.append((url, menuItem, True))
    xbmcplugin.addDirectoryItems(__handle__, menuItems, len(menuItems))
    xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_NONE) #不排序
    xbmcplugin.endOfDirectory (__handle__)

#列出搜索视频列表
def list_search_results(query, source_name: str, page: int):
    if not (video_sources[source_name]['enable'] == 'true'):
        mainMenu()
        return
    module = __import__(f'resources.lib.sources.{source_name}', fromlist=[''])
    current_source = module.Source(video_sources[source_name]['url'])
    if (query == None):
        kb = xbmc.Keyboard('', '输入搜索关键词')
        kb.doModal()
        if not kb.isConfirmed():
            return
        query = kb.getText() #用户输入
    results = current_source.search_parser(query, page)
    menuItems = []
    #获取图片headers
    headers_str = '|'
    for header_key in results['cover_headers']:
        headers_str = headers_str + f'{header_key}={results["cover_headers"][header_key]}&'
    if (headers_str == '|'):
        headers_str == ''
    else:
        headers_str.strip('&')
    #结果
    for result in results['results']:
        url = f"{__url__}?action=list_plays&source={source_name}&id={result['id']}"
        menuItem = xbmcgui.ListItem(label = str(result['title']))
        cover_url = result['cover'] + headers_str
        menuItem.setArt({'poster': cover_url})
        menuItem.setInfo('video', {'plot': fmt.newline.join(result['description'])})
        #添加到收藏菜单
        favorite_data = {'title': str(result['title']), 'cover': cover_url, 'description': fmt.newline.join(result['description']), 'url': url}
        favorite_url = f"{__url__}?action=add_favorite&data={base64.b64encode(json.dumps(favorite_data).encode('utf-8')).decode('utf-8')}"
        menuItem.addContextMenuItems([("添加到收藏", f'RunPlugin({favorite_url})')])
        menuItems.append((url, menuItem, True))
    #下一页
    if len(results['results']) > 0:
        menuItem = xbmcgui.ListItem (label = fmt.color('>>下一页', 'yellow'))
        url = f"{__url__}?action=list_search_results&source={source_name}&query={query}&page={page + 1}"
        menuItems.append((url, menuItem, True))
    xbmcplugin.addDirectoryItems(__handle__, menuItems, len(menuItems))
    xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_NONE) #不排序
    xbmcplugin.endOfDirectory (__handle__)

#列出所有集
def list_plays(source_name: str, id: str):
    if not (video_sources[source_name]['enable'] == 'true'):
        mainMenu()
        return
    module = __import__(f'resources.lib.sources.{source_name}', fromlist=[''])
    current_source = module.Source(video_sources[source_name]['url'])
    results = current_source.playlist_parser(id)
    #获取图片url
    headers_str = '|'
    for header_key in results['cover_headers']:
        headers_str = headers_str + f'{header_key}={results["cover_headers"][header_key]}&'
    if (headers_str == '|'):
        headers_str == ''
    else:
        headers_str.strip('&')
    cover_url = results['cover'] + headers_str
    #获取详情
    description = fmt.bold(results['title']) + fmt.newline + fmt.newline.join(results['description'])
    menuItems = []
    for result in results['results']:
        #通过action url传递信息，作为播放源的信息
        cover_base64 = quote(base64.b64encode(cover_url.encode('utf-8')).decode('utf-8'))
        description_base64 = quote(base64.b64encode(description.encode('utf-8')).decode('utf-8'))
        url = f"{__url__}?action=list_sources&source={source_name}&id={result['id']}&title={result['title']}&cover={cover_base64}&description={description_base64}"
        menuItem = xbmcgui.ListItem(label = str(result['title']))
        menuItem.setArt({'poster': cover_url}) #cover
        menuItem.setInfo('video', {'plot': description}) #详情
        menuItems.append((url, menuItem, True))
    xbmcplugin.addDirectoryItems(__handle__, menuItems, len(menuItems))
    xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_NONE) #不排序
    xbmcplugin.endOfDirectory (__handle__)

#列出播放源
def list_sources(source_name: str, id: str, title: str, cover: str, description: str):
    if not (video_sources[source_name]['enable'] == 'true'):
        mainMenu()
        return
    module = __import__(f'resources.lib.sources.{source_name}', fromlist=[''])
    current_source = module.Source(video_sources[source_name]['url'])
    play_urls = current_source.play_parser(id) #获取播放源链接
    menuItems = []
    for url in play_urls:
        #获取headers
        headers_str = '|'
        for header_key in url['headers']:
            headers_str = headers_str + f'{header_key}={url["headers"][header_key]}&'
        if (headers_str == '|'):
            headers_str == ''
        else:
            headers_str.strip('&')
        play_url = url['url'] + headers_str
        menuItem = xbmcgui.ListItem(label = f"{title}-{url['title']}", path = play_url)
        menuItem.setArt({'poster': base64.b64decode(cover.encode('utf-8')).decode('utf-8')})
        menuItem.setInfo('video', {'genre': video_sources[source_name]['name'], 'plot': base64.b64decode(description.encode('utf-8')).decode('utf-8')})
        menuItems.append((play_url, menuItem, False))
    xbmcplugin.addDirectoryItems(__handle__, menuItems, len(menuItems))
    xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_NONE) #不排序
    xbmcplugin.endOfDirectory (__handle__)

def add_favorite(data_str: str):
    data = json.loads(base64.b64decode(data_str.encode('utf-8')).decode('utf-8'))
    con = sqlite3.connect(os.path.join(xbmcaddon.Addon("plugin.video.videoscrapers").getAddonInfo("path"), 'resources/favorite.db'))
    cur = con.cursor()
    cur.executemany("INSERT INTO favorite VALUES(?, ?, ?, ?)",
                    [(data['title'], data['cover'], data['description'], data['url'])])
    con.commit()
    cur.close()
    con.close()

def list_favorite():
    con = sqlite3.connect(os.path.join(xbmcaddon.Addon("plugin.video.videoscrapers").getAddonInfo("path"), 'resources/favorite.db'))
    cur = con.cursor()
    menuItems = []
    #列出所有
    results = cur.execute("SELECT title, cover, description, url FROM favorite WHERE title like '%%'")
    for result in results.fetchall():
        url = result[3]
        menuItem = xbmcgui.ListItem(label = result[0])
        menuItem.setArt({'poster': result[1]})
        menuItem.setInfo('video', {'plot': result[2]})
        #添加到收藏菜单
        menu_url = f"{__url__}?action=remove_favorite&data={result[0]}"
        menuItem.addContextMenuItems([("从收藏移除", f'RunPlugin({menu_url})')])
        menuItems.append((url, menuItem, True))
    xbmcplugin.addDirectoryItems(__handle__, menuItems, len(menuItems))
    xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_NONE) #不排序
    xbmcplugin.endOfDirectory (__handle__)
    cur.close()
    con.close()

def remove_favorite(title: str):
    con = sqlite3.connect(os.path.join(xbmcaddon.Addon("plugin.video.videoscrapers").getAddonInfo("path"), 'resources/favorite.db'))
    cur = con.cursor()
    cur.execute(f"DELETE FROM favorite WHERE title like '{title}'")
    con.commit()
    cur.close()
    con.close()
    return

#url
def routes(paramString):
    params = dict(parse_qsl(paramString[1 :]))
    if params:
        action = params['action']
        if action == 'list_indexs': #列出类别
            list_indexs(params['source'])
        elif action == 'list_videos': #列出指定类别下条目
            list_videos(params['source'], params['id'], int(params['page']))
        elif action == 'list_plays': #列出集
            list_plays(params['source'], params['id'])
        elif action == 'list_sources': #列出播放链接
            list_sources(params['source'], params['id'], params['title'], unquote(params['cover']), unquote(params['description']))
        elif action == 'list_search_results': #列出搜索结果
            if 'query' in params:
                list_search_results(params['query'], params['source'], int(params['page'])) #用于加载下一页
            else:
                list_search_results(None, params['source'], int(params['page'])) #用于键盘输入搜索
        elif action == 'add_favorite':
            add_favorite(params['data'])
        elif action == 'list_favorite':
            list_favorite()
        elif action == 'remove_favorite':
            remove_favorite(params['data'])
    else :
        mainMenu()

if __name__ == '__main__' :
    routes(sys.argv[2])