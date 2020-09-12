import os
import xlrd
import re
import pyperclip
from openpyxl import Workbook
from pathlib import Path
from rich import print


def init():
    try:
        path = Path('origindata/')
        if path.is_dir() is False:
            os.mkdir(path)
        a = pyperclip.paste()
        if a == 'debugturnon':
            return True
    except Exception as e:
        print('初始化[bold red]失败[/bold red]，原因：' + str(e))


def dealxlsx(path: str, name: str, canprint: bool):
    try:
        workbook = xlrd.open_workbook(path + '/' + name)
        sheet_name = workbook.sheet_names()[0]
        print('\n读取的Excel表名为：' + sheet_name)
        sheet = workbook.sheet_by_index(0)
        allrows = sheet.nrows
        allcols = sheet.ncols - 1
        print('一共有：' + str(allcols) + '列  ' + str(allrows) + '行（第一列时间未计入统计）')
        secend = input('请输入基准点（第几秒）：')
        valueforall = input('请输入一个基准值（自定即可）：')
        startpoint = int(secend)
        startvalue = sheet.cell(startpoint, 0).value
        print('所选取的修改起始点为：' + str(int(startvalue)) + '秒的数据')
        wb = Workbook()  # 引入result.xlsx工作表
        result = wb["Sheet"]
        if result.cell(1, 1).value is None:  # 因为两个库起始index不同，先设置一下第一行
            result.cell(1, 1).value = 0
            if canprint is True:
                print('\n1列1行 写入时间：0秒\n')
        for col in range(1, allcols + 1):  # 获取数据excel每列与基准值的差值
            minus = sheet.cell(startpoint, col).value - float(valueforall)
            print('第' + str(col) + '列截取的起始数据点为：' +
                  str(sheet.cell(startpoint, col).value))
            print('第' + str(col) + '列与基准值的差为：' + str(minus) + '\n')
            vcols = sheet.col_values(col)
            result.cell(1, col + 1).value = float(
                valueforall)  # 因为两个库起始index不同，先设置一下第一行
            if canprint is True:
                print(
                    str(col + 1) + '列1行' + '写入数据：' + str(float(valueforall)) +
                    '\n')
            for num in range(1, len(vcols)):  # 获取数据excel每行的数据，写入index+1的位置
                if result.cell(num + 1, 1).value is None:
                    result.cell(num + 1, 1).value = int(num)
                    if canprint is True:
                        print('1列' + str(num + 1) + '行 写入时间：' + str(int(num)) +
                              '秒' + '\n')
                if num > startpoint:
                    if canprint is True:
                        print(
                            str(col + 1) + '列' + str(num + 1) + '行' + '读取数据：' +
                            str(sheet.cell(num, col).value))
                    result.cell(num + 1, col +
                                1).value = sheet.cell(num, col).value - minus
                    if canprint is True:
                        print(
                            str(col + 1) + '列' + str(num + 1) + '行' + '写入数据：' +
                            str(float(sheet.cell(num, col).value - minus)) +
                            '\n')
                else:
                    if canprint is True:
                        print(
                            str(col + 1) + '列' + str(num + 1) + '行' + '读取数据：' +
                            str(sheet.cell(num, col).value))
                    result.cell(num + 1, col + 1).value = float(valueforall)
                    if canprint is True:
                        print(
                            str(col + 1) + '列' + str(num + 1) + '行' + '写入数据：' +
                            str(float(valueforall)) + '\n')
        wb.save("result.xlsx")
        print('[bold green]处理完成[/bold green]')
    except Exception as e:
        print('处理excel[bold red]失败[/bold red]，原因：' + str(e))


def main():
    try:
        canprint = False
        if init() is True:
            canprint = True
        name = input('请输入要处理的文件名')
        if re.search(r'xlsx|xls', name) is None:
            namewithsuffix4 = name + '.xlsx'
            path = Path('origindata/' + namewithsuffix4)
            if path.is_file() is True:
                dealxlsx('origindata/', namewithsuffix4, canprint)
            else:
                namewithsuffix3 = name + '.xls'
                path = Path('origindata/' + namewithsuffix3)
                if path.is_file() is True:
                    dealxlsx('origindata/', namewithsuffix3, canprint)
        else:
            dealxlsx('origindata/', name, canprint)
        input('如有问题请前往 https://github.com/evilbutcher/Python 提出issue，请按任意键退出')
    except Exception as e:
        print('主函数运行[bold red]出现错误[/bold red]，原因：' + str(e))


if __name__ == "__main__":
    main()
