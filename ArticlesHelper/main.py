import requests
import os
import re
from rich.console import Console
from rich import print
from rich.table import Column, Table
from pathlib import Path
from bs4 import BeautifulSoup


def init():
    # 判断目录
    path = Path('ArticlesHelper/articles/')
    if path.is_dir() is False:
        os.mkdir(path)


def downloadfile(name, doi, url):
    pdf = requests.get(url)
    # 保存文件
    if pdf.status_code == 200:
        with open('ArticlesHelper/articles/' + name, 'wb') as f:
            f.write(pdf.content)
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("文件名")
        table.add_column("状态")
        table.add_row(name, '[bold green]下载完成[/bold green]')
        console.print(table)
    else:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("文件名")
        table.add_column("状态")
        table.add_row(doi, '[bold red]下载失败[/bold red]')
        console.print(table)
        print(pdf)


def stwgetdllink(link):
    data = requests.get(link)
    # 获取下载链接
    html = data.text
    afterhtml = BeautifulSoup(html, 'html.parser')
    div = afterhtml.find('iframe', id='pdf')
    if div is None:
        print('[bold red]未找到文献[/bold red]')
    else:
        pdflink = div.get('src')
        # print(re.match(r'https:', pdflink))
        if re.match(r'https:', pdflink) is None:
            postlink = 'https:' + pdflink
        else:
            postlink = pdflink
    print('下载链接：' + postlink)
    return postlink


if __name__ == "__main__":
    init()
    console = Console()
    doi = input('请输入DOI：')
    hostlink = 'https://sci-hub.tw/'
    link = hostlink + doi
    filename = doi.replace('/', '_') + '.pdf'
    print('DOI：' + doi)
    print('保存文件名：' + filename)
    print('请求链接：' + link)
    downloadfile(filename, doi, stwgetdllink(link))
    input('按任意键退出')
