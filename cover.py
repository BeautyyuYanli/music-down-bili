import requests, os, eyed3
from bs4 import BeautifulSoup as bs
def get_cover(url):
    with requests.get(url) as getimage:
        return getimage.content
def add_cover(img, mp3path):
    audiofile = eyed3.load(mp3path)
    if (audiofile.tag == None):
        audiofile.initTag()
    audiofile.tag.images.set(3, img, 'image/jpeg')
    audiofile.tag.save()
if __name__ == '__main__':
    url = 'https://www.bilibili.com/video/BV1FV411i7ok'
    add_cover(get_cover(url), 'test.mp3')