from urllib import request
from bs4 import BeautifulSoup

import requests
import threading

gLock = threading.Lock()

IMGS_URL = []

def getHTMLText(url):
    r = requests.get(url)
    try:
        r.raise_for_status
        return r.content
    except:
        return ''

def getHTMLInfo(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        imgs = soup.find_all('img', attrs={'class':'img-responsive lazy image_dta'})
        for img in imgs:
            IMGS_URL.append(img['data-original'])
        return IMGS_URL
    except:
        return IMGS_URL

def downloadImages(url, path):
    '下载传入url对应的图片，并存入指定路径中'
    fn = url.split('/')[-1]
    path = path + fn
    try:
        request.urlretrieve(url, filename=path)
    except:
        print('下载出错')

def producer():
    '爬取所有需要的url'
    global IMGS_URL
    base_url = 'http://www.doutula.com/photo/list/?page='
    urls = (base_url + str(x) for x in range(2))
    for x in urls:
        html = getHTMLText(x)
        gLock.acquire()
        getHTMLInfo(html)
        print(len(IMGS_URL))
        gLock.release()
    

def customer():
    global IMGS_URL
    path = 'images/'
    while True:
        if len(IMGS_URL) == 0:
            print('+'*50)
            continue
        gLock.acquire()
        url = IMGS_URL.pop()
        downloadImages(url, path)
        gLock.release()
    

def main():
    for x in range(3):
        th = threading.Thread(target=producer)
        th.start()

    for x in range(5):
        th = threading.Thread(target=customer)
        th.start()

if __name__ == '__main__':
    main()
    print(IMGS_URL)