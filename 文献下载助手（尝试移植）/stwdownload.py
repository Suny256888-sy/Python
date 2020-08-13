import requests
import os
from bs4 import BeautifulSoup

if __name__=="__main__":
  doi = '10.2967/jnumed.115.160960'
  path = 'articles/'
  hostlink = 'https://sci-hub.tw/'
  link = hostlink + doi
  filename = doi

  print(link)
  data = requests.get(url=link)
  html = data.text
  afterhtml = BeautifulSoup(html, 'html.parser')
  pdflink = afterhtml.find('iframe', id='pdf').get("src")
  pdf = requests.get(pdflink)


 

  print(pdflink)
  input("按任意键结束")
