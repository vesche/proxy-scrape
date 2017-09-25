#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# proxyscrape.py
# https://github.com/vesche
#

import bs4
import pytesseract
import requests
import subprocess

from io import BytesIO
from PIL import Image

BASE_URL = 'https://www.torvpn.com'
PROXY_LOC = '/en/proxy-list'


def process_image(img):
    img.save('/tmp/tmp_img1.png')
    command = 'convert /tmp/tmp_img1.png -resize 200% /tmp/tmp_img2.png'
    subprocess.call(command.split())
    img = Image.open('/tmp/tmp_img2.png')

    cleanup = 'rm /tmp/tmp_img1.png /tmp/tmp_img2.png'
    subprocess.call(cleanup.split())

    return img


def main():
    page = requests.get('{}{}'.format(BASE_URL, PROXY_LOC)).content
    soup = bs4.BeautifulSoup(page, 'html.parser')
    table = soup.find('table', attrs={'class': 'table table-striped'})
    rows = table.find_all('tr')

    data = []
    for row in rows:
        cols = row.find_all('td')
        data.append([ele for ele in cols])

    proxy_dicts = []
    for i in range(len(data)):
        try:
            d = { 'img_pic':    data[i][1].find('img')['src'],
                  'port':       data[i][2].text,
                  'country':    data[i][3].text.split('\n')[1],
                  'proxy_type': data[i][4].text.lower() }
            proxy_dicts.append(d)
        except IndexError:
            continue

    # convert image to IP
    for i in range(len(proxy_dicts)):
        d = proxy_dicts[i]
        response = requests.get('{}{}'.format(BASE_URL, d['img_pic']))
        img = Image.open(BytesIO(response.content))

        # double image size to correct OCR errors
        img = process_image(img)
        
        ip = pytesseract.image_to_string(img)
        d['ip'] = ip

    # print in proxychains format
    for d in proxy_dicts:
        print('{} {:15} {:5} # {}'.format(
            d['proxy_type'], d['ip'], d['port'], d['country']))


if __name__ == '__main__':
    main()
