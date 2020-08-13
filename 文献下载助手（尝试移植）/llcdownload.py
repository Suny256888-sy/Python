import requests
from bs4 import BeautifulSoup

doi = ''

target = 'https://libgen.lc/scimag/ads.php?doi=' + doi
req = requests.get(url=target)
html = req.text
bf = BeautifulSoup(html, 'html.parser')
texts = bf.find('iframe', id='pdf').get("src")
print(texts)
input("按任意键结束")