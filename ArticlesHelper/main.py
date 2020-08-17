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
    try:
        response = urlopen(url)
        # This will break if the response doesn't contain content length
        progress.update(task_id, total=int(response.info()["Content-length"]))
        with open(path, "wb") as dest_file:
            progress.start_task(task_id)
            for data in iter(partial(response.read, 32768), b""):
                dest_file.write(data)
                progress.update(task_id, advance=len(data))
    except Exception as e:
        print('下载' + task_id + '出错啦，原因：' + str(e))


def download(urls, dest_dir):
    try:
        print('\n下载进度')
        with progress:
            with ThreadPoolExecutor(max_workers=4) as pool:
                for key, value in urls.items():
                    if value is None:
                        continue
                    filename = key.replace('/', '_') + '.pdf'
                    dest_path = os.path.join(dest_dir, filename)
                    task_id = progress.add_task("download",
                                                filename=filename,
                                                start=False)
                    pool.submit(copy_url, task_id, value, dest_path)
    except Exception as e:
        print('队列任务出错啦，原因：' + str(e))


def parsehtml(name):
    print('\n开始解析' + name)
    try:
        with open('./records/' + name, mode='r', encoding='utf-8') as f:
            content = f.read()
        parse = BeautifulSoup(content, 'html.parser')
        for k in parse.find_all('td'):
            # print(k.string)
            if k.string == 'DI ':
                dois.append(k.find_next_sibling().string)
    except Exception as e:
        print('解析过程出现错误，原因：' + str(e))


def init():
    print('检测更新中...')
    version = 2.3
    urlgithub = 'https://raw.githubusercontent.com/evilbutcher/Python/master/ArticlesHelper/release.json'
    try:
        update = requests.get(urlgithub)
        ver = update.json()
        if ver['releases'][0]['version'] > version:
            print('[bold yellow]更新[/bold yellow]啦！从GitHub获取更新详情成功！\n最新版本是：' +
                  str(ver['releases'][0]['version']))
            print('更新内容是：' + ver['releases'][0]['details'])
            print('可前往项目地址：https://github.com/evilbutcher/Python 查看Releases')
        else:
            print('检测更新完成，暂无更新')
    except (Exception):
        urlgitee = 'https://gitee.com/evilbutcher/Python/raw/master/ArticlesHelper/release.json'
        try:
            update = requests.get(urlgitee)
            ver = update.json()
            if ver['releases'][0]['version'] > version:
                print('[bold red]更新[/bold red]啦！从Gitee获取更新详情成功！\n最新版本是：' +
                      str(ver['releases'][0]['version']))
                print('更新内容是：' + ver['releases'][0]['details'])
                print(
                    '可前往项目地址：https://github.com/evilbutcher/Python 查看Releases')
            else:
                print('检测更新完成，暂无更新')
        except Exception as e:
            print('检测更新失败，原因：')
            print(str(e))
    # 判断目录
    articlespath = Path('articles/')
    recordpath = Path('records/')
    try:
        if articlespath.is_dir() is False:
            os.mkdir(articlespath)
        if recordpath.is_dir() is False:
            os.mkdir(recordpath)
        isexist = False
        waitparse = []
        for root, dirs, files in os.walk(recordpath):
            if files is not None:
                for file in files:
                    if re.search(r'.html', file):
                        waitparse.append(file)
                        print('发现[bold yellow]待解析[/bold yellow]文件：' +
                              os.path.join(file))
                        isexist = True
        if isexist is True:
            if len(waitparse) == 1:
                go = input('\n是否尝试进行解析？(请输入y/n)')
                if go == 'y':
                    name = waitparse[0]
                    parsehtml(name)
            else:
                name = input('\n是否尝试解析？(请输入要解析的文件名称；不解析请输入n)')
                if name == 'n':
                    return
                else:
                    parsehtml(name)
    except Exception as e:
        print('获取目录出错啦，错误原因：' + str(e))


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
        print('获取下载链接[bold green]成功[/bold green]：' + postlink)
        urls[doi] = postlink
        return True
    except Exception as e:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("文件名")
        table.add_column("状态")
        table.add_column("原因")
        table.add_row(name, '[bold red]未找到文献[/bold red]', str(e))
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
        print('获取下载链接[bold green]成功[/bold green]：' + postlink)
        urls[doi] = postlink
        return True
    except Exception as e:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("文件名")
        table.add_column("状态")
        table.add_column("原因")
        table.add_row(name, '[bold red]未找到文献[/bold red]', str(e))
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
        print('获取下载链接[bold green]成功[/bold green]：' + pdflink)
        urls[doi] = pdflink
        return True
    except Exception as e:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("文件名")
        table.add_column("状态")
        table.add_column("原因")
        table.add_row(name, '[bold red]未找到文献[/bold red]', str(e))
        console.print(table)
        urls[doi] = None
        return False


def continuousgetlink(name, doi, i):
    if (i + 1) % 3 == 1:
        if stwgetdllink(name, doi) is False:
            print('自动更换地址[bold green]重新获取[/bold green]')
            if lbggetdllink(name, doi) is False:
                print('自动更换地址[bold green]重新获取[/bold green]')
                if ssegetdllink(name, doi) is False:
                    print('很抱歉，此文献[bold red]未找到[/bold red]')
    elif (i + 1) % 3 == 2:
        if lbggetdllink(name, doi) is False:
            print('自动更换地址[bold green]重新获取[/bold green]')
            if ssegetdllink(name, doi) is False:
                print('自动更换地址[bold green]重新获取[/bold green]')
                if stwgetdllink(name, doi) is False:
                    print('很抱歉，此文献[bold red]未找到[/bold red]')
    else:
        if ssegetdllink(name, doi) is False:
            print('自动更换地址[bold green]重新获取[/bold green]')
            if lbggetdllink(name, doi) is False:
                print('自动更换地址[bold green]重新获取[/bold green]')
                if stwgetdllink(name, doi) is False:
                    print('很抱歉，此文献[bold red]未找到[/bold red]')


def checkdownload(dois):
    try:
        redownload = []
        dldois = []
        for doi in dois:
            doi.replace('_', '/')
        articlespath = Path('articles/')
        for root, dirs, files in os.walk(articlespath):
            if len(files) == 0:
                print(dois)
                print('\n[bold red]全部下载失败[/bold red]，可稍后尝试下载或检查网络状况重新下载。')
            else:
                for file in files:
                    dldoi = file.replace('_', '/').replace('.pdf', '')
                    dldois.append(dldoi)
                for doi in dois:
                    if (doi in dldois) is False:
                        redownload.append(doi)
                if len(redownload) != 0:
                    print('\n[bold yellow]部分下载完成[/bold yellow]，下载失败的doi为：')
                    print(redownload)
                else:
                    print('\n[bold green]全部下载完成[/bold green]，恭喜！')
    except Exception as e:
        print('检查下载情况出错啦，原因：' + str(e))


if __name__ == "__main__":
    console = Console()
    print('特别感谢Rich项目 https://github.com/willmcgugan/rich')
    print('作者@evilbutcher')
    dois = []
    init()
    if len(dois) == 0:
        print('\n若为多篇文献请用[bold red]英文逗号[/bold red]分隔')
        doi = input('请输入DOI：')
        dois = list(doi.split(','))
    print('\n开始下载...')
    print('\n[bold yellow]说明[/bold yellow]：提示文献未找到，只是一个接口未找到，会自动更换接口获取下载地址')
    print('\ndoi为：')
    print(dois)
    urls = {}
    for index, value in enumerate(dois):
        filename = value.replace('/', '_') + '.pdf'
        continuousgetlink(filename, value, index)
    print('\n匹配下载链接[bold green]完成[/bold green]，None表示未能获取下载地址')
    print(urls)
    download(urls, './articles/')
    checkdownload(dois)
    input('如有问题请前往 https://github.com/evilbutcher/Python 提出issue，请按任意键退出')
