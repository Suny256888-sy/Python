[![Anurag's github stats](https://github-readme-stats.vercel.app/api?username=evilbutcher)](https://github.com/anuraghazra/github-readme-stats)

# [文献下载小程序](https://github.com/evilbutcher/Python/tree/master/ArticlesHelper)
一开始写了JavaScript版的[文献下载助手](https://github.com/evilbutcher/Code/tree/master/%E6%96%87%E7%8C%AE%E4%B8%8B%E8%BD%BD/%E6%96%87%E7%8C%AE%E4%B8%8B%E8%BD%BD%E5%8A%A9%E6%89%8B)，但这个只能在JSBox上运行，有一定的限制和门槛。
时至今日，我终于捡起来Python，开始着手移植，一边移植一边学python...  
### 关于如何使用
请前往[Releases](https://github.com/evilbutcher/Python/releases)  
For Windows:  
下载最新的文献下载助手小程序.exe。  
For Mac OS:  
因为没有Mac，所以提供了源码，请自行测试，用到的模块有：
```python
import requests
import os
import re
from rich.console import Console
from rich import print
from rich.table import Table
from pathlib import Path
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from urllib.request import urlopen
from rich.progress import (
    BarColumn,
    DownloadColumn,
    TextColumn,
    TransferSpeedColumn,
    TimeRemainingColumn,
    Progress,
    TaskID,
)
```
首次运行，会在同级目录生成两个文件夹，一个是articles，用于存储下载的文献，另一个是records，用于存储下载的Web of Science文献记录。
#### 如何下载Web of Science文献记录
选中文献后，导出格式中选择html，然后将下载的html文件转存到同级目录的records文件夹中。  
![Download record](https://raw.githubusercontent.com/evilbutcher/Python/master/ArticlesHelper/How_to_Use/download_record.gif)
#### 如何解析记录
如果程序检测到在records中，存在.html格式的文件，就会自动将名称列出来，提示是否进行解析，输入 y 则会执行解析，n 则会返回手动输入doi号下载。
如果存在records中存在个html文件，可直接输入全称如 savedrecs.html 进行解析，不解析请输入 n 。  
![Parse record](https://raw.githubusercontent.com/evilbutcher/Python/master/ArticlesHelper/How_to_Use/parse_records.gif)
#### 如何手动下载
直接输入doi号即可下载，多个doi请用英文逗号“,”进行分割，例如 10.1016/j.snb.2013.07.010,10.1016/j.snb.2010.12.010,10.1039/c5cs00424a。  
![Download manually](https://raw.githubusercontent.com/evilbutcher/Python/master/ArticlesHelper/How_to_Use/download_manually.gif)
#### 自动检测更新
如果有更新，软件会自动弹出更新提示，可前往[Releases](https://github.com/evilbutcher/Python/releases)地址进行更新。  
![Check update](https://raw.githubusercontent.com/evilbutcher/Python/master/ArticlesHelper/How_to_Use/check_update.gif)

### 现已支持
1.根据doi进行文献下载和保存  
2.下载异常判断  
3.批量下载  
4.自动交替请求下载  
5.下载失败自动更换地址  
6.进度条  
7.自动检测更新  
8.解析Web of Science文献记录  
9.下载情况检查

### 特别感谢：
[@Rich](https://github.com/willmcgugan/rich)