import sys
import xbmcplugin

__handle__ = int(sys.argv[1])

video_sources = {
    'yhdm': {
        'name': '樱花动漫',
        'color': 'pink',
        'url': xbmcplugin.getSetting(__handle__, 'yhdm-url'), #源链接
        'enable': xbmcplugin.getSetting(__handle__, 'yhdm') #是否启用
    },
    'meijutt': {
        'name': '美剧天堂',
        'color': 'blue',
        'url': xbmcplugin.getSetting(__handle__, 'meijutt-url'), #源链接
        'enable': xbmcplugin.getSetting(__handle__, 'meijutt') #是否启用
    },
    'dmd': {
        'name': '动漫岛',
        'color': 'pink',
        'url': xbmcplugin.getSetting(__handle__, 'dmd-url'), #源链接
        'enable': xbmcplugin.getSetting(__handle__, 'dmd') #是否启用
    },
    'lbbb': {
        'name': '萝卜影视',
        'color': 'white',
        'url': xbmcplugin.getSetting(__handle__, 'lbbb-url'), #源链接
        'enable': xbmcplugin.getSetting(__handle__, 'lbbb') #是否启用
    }
}