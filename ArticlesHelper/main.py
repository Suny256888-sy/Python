import requests
import os
# import re
from pathlib import Path
from bs4 import BeautifulSoup

if __name__ == "__main__":
    doi = '10.1021/ja0530016'
    hostlink = 'https://sci-hub.tw/'
    link = hostlink + doi
    filename = doi.replace('/', '_') + ".pdf"
    print(filename)
    # 判断目录
    path = Path('ArticlesHelper/articles/')
    if path.is_dir() is False:
        os.mkdir(path)
    # 下载文件
    print(link)
    data = requests.get(url=link)
    html = data.text
    afterhtml = BeautifulSoup(html, 'html.parser')
    div = afterhtml.find('iframe', id='pdf')
    if div is None:
        print('未找到文献')
    else:
        pdflink = div.get("src")
        pdf = requests.get(pdflink)
        # 保存文件
        with open('ArticlesHelper/articles/' + filename, 'wb') as f:
            f.write(pdf.content)
        f.close()
        print(filename + ' 下载完成')
