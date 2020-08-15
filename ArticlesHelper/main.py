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

progress = Progress(
    TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
    BarColumn(bar_width=None),
    "[progress.percentage]{task.percentage:>3.1f}%",
    "•",
    DownloadColumn(),
    "•",
    TransferSpeedColumn(),
    "•",
    TimeRemainingColumn(),
)


def copy_url(task_id: TaskID, url: str, path: str) -> None:
    """Copy data from a url to a local file."""
    response = urlopen(url)
    # This will break if the response doesn't contain content length
    progress.update(task_id, total=int(response.info()["Content-length"]))
    with open(path, "wb") as dest_file:
        progress.start_task(task_id)
        for data in iter(partial(response.read, 32768), b""):
            dest_file.write(data)
            progress.update(task_id, advance=len(data))


def download(urls, dest_dir):
    """Download multuple files to the given directory."""
    with progress:
        with ThreadPoolExecutor(max_workers=4) as pool:
            try:
                for key, value in urls.items():
                    filename = key.replace('/', '_') + '.pdf'
                    dest_path = os.path.join(dest_dir, filename)
                    task_id = progress.add_task("download",
                                                filename=filename,
                                                start=False)
                    pool.submit(copy_url, task_id, value, dest_path)
            except (Exception):
                print(key + value + '出错啦')


def init():
    # 判断目录
    path = Path('./articles/')
    if path.is_dir() is False:
        os.mkdir(path)


def stwgetdllink(name, doi):
    try:
        hostlink = 'https://sci-hub.tw/'
        link = hostlink + doi
        data = requests.get(link)
        # 获取下载链接
        html = data.text
        afterhtml = BeautifulSoup(html, 'html.parser')
        div = afterhtml.find('iframe', id='pdf')
        pdflink = div.get('src')
        if re.match(r'https:', pdflink) is None:
            postlink = 'https:' + pdflink
        else:
            postlink = pdflink
        print('下载链接：' + postlink)
        urls[doi] = postlink
        return True
    except (Exception):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("文件名")
        table.add_column("状态")
        table.add_row(name, '[bold red]未找到文献[/bold red]')
        console.print(table)
        urls[doi] = None
        return False


def ssegetdllink(name, doi):
    try:
        hostlink = 'https://sci-hub.se/'
        link = hostlink + doi
        data = requests.get(link)
        # 获取下载链接
        html = data.text
        afterhtml = BeautifulSoup(html, 'html.parser')
        div = afterhtml.find('iframe', id='pdf')
        pdflink = div.get('src')
        if re.match(r'https:', pdflink) is None:
            postlink = 'https:' + pdflink
        else:
            postlink = pdflink
        print('下载链接：' + postlink)
        urls[doi] = postlink
        return True
    except (Exception):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("文件名")
        table.add_column("状态")
        table.add_row(name, '[bold red]未找到文献[/bold red]')
        console.print(table)
        urls[doi] = None
        return False


def lbggetdllink(name, doi):
    try:
        hostlink = 'https://libgen.lc/scimag/ads.php?doi='
        link = hostlink + doi
        data = requests.get(link)
        # 获取下载链接
        html = data.text
        afterhtml = BeautifulSoup(html, 'html.parser')
        div = afterhtml.find('a')
        pdflink = div.get('href')
        print('下载链接：' + pdflink)
        urls[doi] = pdflink
        return True
    except (Exception):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("文件名")
        table.add_column("状态")
        table.add_row(name, '[bold red]未找到文献[/bold red]')
        console.print(table)
        urls[doi] = None
        return False


def continuousgetlink(name, doi, i):
    if (i + 1) % 3 == 1:
        if stwgetdllink(name, doi) is False:
            if lbggetdllink(name, doi) is False:
                ssegetdllink(name, doi)
    elif (i + 1) % 3 == 2:
        if lbggetdllink(name, doi) is False:
            if ssegetdllink(name, doi) is False:
                stwgetdllink(name, doi)
    else:
        if ssegetdllink(name, doi) is False:
            if lbggetdllink(name, doi) is False:
                stwgetdllink(name, doi)


if __name__ == "__main__":
    init()
    console = Console()
    print('特别感谢rich项目 https://github.com/willmcgugan/rich \n作者@evilbutcher\n\n若为多篇文献请用[bold red]英文逗号[/bold red]分隔')
    doi = input('请输入DOI：')
    print('\n开始下载...\n[bold yellow]说明[/bold yellow]：如果提示文献未找到，可暂时不用管，只是其中一个接口未找到文献，会自动更新接口获取下载地址')
    dois = list(doi.split(','))
    print('\n输入的doi为：')
    print(dois)
    urls = {}
    for index, value in enumerate(dois):
        filename = value.replace('/', '_') + '.pdf'
        continuousgetlink(filename, value, index)
    print('\n匹配下载链接[bold green]完成[/bold green]')
    print(urls)
    print('\n下载进度')
    download(urls, './articles/')
    input('下载完成，如遇到问题欢迎前往 https://github.com/evilbutcher/Python 提出issue，请按任意键退出')
