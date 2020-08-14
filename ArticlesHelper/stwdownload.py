import requests
import os
from pathlib import Path
from bs4 import BeautifulSoup

if __name__ == "__main__":
    doi = '10.1021/ja0530016'
    hostlink = 'https://sci-hub.tw/'
    link = hostlink + doi
    filename = doi.replace('/', '_') + ".pdf"
    # 判断目录
    path = Path('ArticlesHelper/articles/')
    exist = path.is_dir()
    if exist == False:
        os.mkdir(path)
    print(link)
    # 下载文件
    data = requests.get(url=link)
    html = data.text
    afterhtml = BeautifulSoup(html, 'html.parser')
    pdflink = afterhtml.find('iframe', id='pdf').get("src")
    pdf = requests.get(pdflink)
    # 保存文件
    with open('ArticlesHelper/articles/' + filename, 'wb') as f:
        f.write(pdf.content)
        f.close()
