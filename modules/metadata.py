import requests
import os
import eyed3

def addTag(mp3path, title, cover, album):
    audiofile = eyed3.load(mp3path)
    if (audiofile.tag == None):
        audiofile.initTag()
    audiofile.tag.images.set(3, cover, 'image/jpeg')
    audiofile.tag.title = title
    audiofile.tag.album = album
    audiofile.tag.save()

if __name__ == '__main__':
    addTag('../output/时光盲盒【2021拜年纪单品】.mp3', title='test', cover=requests.get(
        'https://i0.hdslb.com/bfs/archive/1b72fbea9a769df4e10b45dc9fdc30c6dba2d2e0.jpg').content)
