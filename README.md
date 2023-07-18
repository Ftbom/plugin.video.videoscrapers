# Video Scrapers

**支持Kodi v19+**

可扩展的Kodi插件，用于从视频网站爬取视频

## 插件开发

* 在`resources/lib/sources`目录下添加python文件，用于爬虫
  >以樱花动漫为例，添加`yhdm.py`
* 在`resources/settings.xml`中添加设置项
  >```xml
  ><category label="樱花动漫">
  >    <setting id="yhdm" type="bool" label="启用" default="true"/>
  >    <setting id="yhdm-url" type="text" label="域名" default="http://www.yinghuacd.com"/>
  ></category>
  >```
* 在`resources/lib/sources/__init__.py`中添加源信息
* >```python
  >'yhdm': { #与文件名相同
  >    'name': '樱花动漫',  #视频源显示名称
  >    'color': 'pink',  #视频源显示名称的颜色
  >    'url': xbmcplugin.getSetting(__handle__, 'yhdm-url'), #源链接
  >    'enable': xbmcplugin.getSetting(__handle__, 'yhdm') #是否启用
  >},
  >```

### 爬虫代码

在爬虫代码中定义类，类名`Source`，至少包含以下方法和属性：

`Source()`
* `self.categroies`
  * 字典数据，包括视频源支持的分类
  * 数据格式：`{<分类: str>: <id: str>}`
* `__init__(self, url) -> None`
  * 初始化函数
  * 输入：
    * url -> 网站的网址
* `index_parser(self, id: str, page: int) -> dict`
  * 返回选定分类下的剧集
  * 输入：
    * id -> 分类id
    * page -> 页码
  * 输出格式：
    * `{'cover_headers': <封面的HTTP头: dict>, 'results': [{'title': <剧集标题: str>, 'id': <剧集id: str>, 'cover': <剧集封面: str>, 'description': <剧集描述信息: list>}, ...]}`
      >剧集描述信息为字符串列表，每个列表元素显示为一行文本，支持[Kodi格式化文本](https://kodi.wiki/view/Label_Formatting)
* `search_parser(self, query: str, page: int) -> dict`
  * 返回选定搜索结果的剧集
  * 输入：
    * query -> 查询字符串
    * page -> 页码
  * 输出格式：
    * `{'cover_headers': <封面的HTTP头: dict>, 'results': [{'title': <剧集标题: str>, 'id': <剧集id: str>, 'cover': <剧集封面: str>, 'description': <剧集描述信息: list>}, ...]}`
      >剧集描述信息同上
* `playlist_parser(self, id: str) -> dict`
  * 返回选定剧集下的集信息和剧集详细信息
  * 输入：
    * id -> 剧集id
  * 输出格式：
    * `{'cover': <剧集标题: str>, 'cover_headers': <封面的HTTP头: dict>, 'title': <剧集标题: str>, 'description': <剧集描述信息: list>, 'results': [{'title': <集标题: str>, 'id': <集id: str>}, ...]}`
      >剧集描述信息同上
* `play_parser(self, id: str) -> list`
  * 返回选定集的播放源
  * 输入：
    * id -> 集id
  * 输出格式：
    * `[{'headers': <播放源链接HTTP头: dict>, 'title': <播放源名称: str>, 'url': <播放源链接: str>}, ...]`

### 字符串格式化工具

在`resources/lib/fmt.py`中对Kodi字符串格式化进行了极其简单的封装，方便使用

### 爬取网页的方式

* 使用requests获取网页
* 如果网页使用Cloudflare保护，可以尝试使用CloudScraper
* 上述两种方式均无效可尝试Web Scrape API

#### CloudScraper

[script.module.cloudscraper](https://github.com/jairoxyz/script.module.cloudscraper)用于绕过Cloudflare的验证，但是效果有限

```python
import cloudscraper2
scraper = cloudscraper2.create_scraper()
```

#### Web Scrape API

通过第三方服务提供的api获取javascript渲染后的html文件

现支持scrapingant、scrapingbee、zenscrape和scraperapi

通过插件设置界面选择要启用的服务以及设置api密钥

### 获取视频播放链接

[script.module.resolveurl](https://github.com/Gujal00/ResolveURL)中内置了很多网站的视频解析代码
>[支持的网站](https://github.com/Gujal00/ResolveURL/tree/master/script.module.resolveurl/lib/resolveurl/plugins)

```python
import resolveurl
if resolveurl.HostedMediaFile(url):
  resolved = resolveurl.resolve(url)
```
