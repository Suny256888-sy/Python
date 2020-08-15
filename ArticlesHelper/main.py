import requests
import os
import re
from rich.console import Console
from rich import print
# from rich.table import Column
from rich.table import Table
from pathlib import Path
from bs4 import BeautifulSoup


def init():
    # 判断目录
    path = Path('./articles/')
    if path.is_dir() is False:
        os.mkdir(path)


def downloadfile(name, doi, url):
    if url is None:
        return False
    try:
        pdf = requests.get(url)
        # 保存文件
        if pdf.status_code == 200:
            with open('./articles/' + name, 'wb') as f:
                f.write(pdf.content)
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("文件名")
            table.add_column("状态")
            table.add_row(name, '[bold green]下载完成[/bold green]')
            console.print(table)
            return True
        else:
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("文件名")
            table.add_column("状态")
            table.add_row(doi, '[bold red]下载失败[/bold red]')
            console.print(table)
            print(pdf)
            return False
    except (Exception):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("文件名")
        table.add_column("状态")
        table.add_row(name, '[bold red]下载文件出错啦[/bold red]')
        console.print(table)
        return False


def stwgetdllink(name, doi):
    try:
        hostlink = 'https://sci-hub.tw/'
        link = hostlink + doi
        print('请求链接：' + link)
        data = requests.get(link)
        # 获取下载链接
        html = data.text
        afterhtml = BeautifulSoup(html, 'html.parser')
        div = afterhtml.find('iframe', id='pdf')
        pdflink = div.get('src')
        # print(re.match(r'https:', pdflink))
        if re.match(r'https:', pdflink) is None:
            postlink = 'https:' + pdflink
        else:
            postlink = pdflink
        print('下载链接：' + postlink)
        return postlink
    except (Exception):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("文件名")
        table.add_column("状态")
        table.add_row(name, '[bold red]未找到文献[/bold red]')
        console.print(table)


def simgetdllink(name, doi):
    try:
        hostlink = 'https://sci-hub.im/'
        link = hostlink + doi
        print('请求链接：' + link)
        data = requests.get(link)
        # 获取下载链接
        html = data.text
        afterhtml = BeautifulSoup(html, 'html.parser')
        div = afterhtml.find('iframe', id='pdf')
        pdflink = div.get('src')
        # print(re.match(r'https:', pdflink))
        if re.match(r'https:', pdflink) is None:
            postlink = 'https:' + pdflink
        else:
            postlink = pdflink
        print('下载链接：' + postlink)
        return postlink
    except (Exception):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("文件名")
        table.add_column("状态")
        table.add_row(name, '[bold red]未找到文献[/bold red]')
        console.print(table)


def lbggetdllink(name, doi):
    try:
        hostlink = 'https://libgen.lc/scimag/ads.php?doi='
        link = hostlink + doi
        print('请求链接：' + link)
        data = requests.get(link)
        # 获取下载链接
        html = data.text
        afterhtml = BeautifulSoup(html, 'html.parser')
        div = afterhtml.find('a')
        pdflink = div.get('href')
        print('下载链接：' + pdflink)
        return pdflink
    except (Exception):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("文件名")
        table.add_column("状态")
        table.add_row(name, '[bold red]未找到文献[/bold red]')
        console.print(table)
        return None


def continuousdl(name, doi, i):
    print((i + 1) % 3)
    if (i + 1) % 3 == 1:
        if downloadfile(name, doi, stwgetdllink(name, doi)) is False:
            if downloadfile(name, doi, lbggetdllink(name, doi)) is False:
                downloadfile(name, doi, simgetdllink(name, doi))
    elif (i + 1) % 3 == 2:
        if downloadfile(name, doi, lbggetdllink(name, doi)) is False:
            if downloadfile(name, doi, simgetdllink(name, doi)) is False:
                downloadfile(name, doi, stwgetdllink(name, doi))
    else:
        if downloadfile(name, doi, simgetdllink(name, doi)) is False:
            if downloadfile(name, doi, lbggetdllink(name, doi)) is False:
                downloadfile(name, doi, stwgetdllink(name, doi))


if __name__ == "__main__":
    init()
    console = Console()
    print('请输入DOI')
    doi = input('若为多个请用英文逗号分隔：')
    dois = list(doi.split(','))
    print(dois)
    for index, value in enumerate(dois):
        filename = value.replace('/', '_') + '.pdf'
        print('DOI：' + value)
        print('保存文件名：' + filename)
        continuousdl(filename, value, index)
    input('按任意键退出')
