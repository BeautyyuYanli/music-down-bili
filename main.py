import feedparser, requests, ffmpeg, time, re, codecs
import downloader, cover
# config
# proxies = { 'http': 'http://127.0.0.1:1081', 'https': 'http://127.0.0.1:1081'}
proxies = {}
rssurl = 'https://rsshub.app/bilibili/fav/10725385/53706285'
# rssurl = 'https://rsshub.app/bilibili/fav/10725385/1173410585'
# bv2av
def bv2av(bvid):
    site = "https://api.bilibili.com/x/web-interface/view?bvid=" + bvid
    lst = codecs.decode(requests.get(site).content, "utf-8").split("\"")
    if int(lst[2][1:-1]) != 0:
        return "视频不存在"
    return 'https://www.bilibili.com/video/av' + lst[16][1:-1]

if __name__ == '__main__':
    # prepare rss
    rss = requests.get(rssurl, proxies=proxies).text
    feed = feedparser.parse(rss)
    # prepare database
    with open('database.pwp', 'r') as f:
        donelist = f.read().split('$')
    # check update
    update_pool = []
    for i in feed.entries:
        i.link = bv2av(i.link.split('/')[-1])
        if i.link not in donelist:
            print(i.link)
            update_pool.append(i)
    # update
    for i in update_pool:
        try:
            # download video
            ftitle = downloader.main(i.link + '?p=1')
            # convert into audio
            mp3path = 'output/' + re.sub(r'[\/\\:*?"<>|]', '', i.title) + '.mp3'
            {ffmpeg
                .input('bilibili_video/' + ftitle + '/' + ftitle + '.flv')
                .output(mp3path, ab = '1080k')
                .run()
            }
            # insert cover
            cover.add_cover(cover.get_cover(i.link), mp3path)
        except:
            print('wrong when downloading: ' + i.link)
        else:
            print('successfully downloaded: ' + i.link)
            # update database
            donelist.append(i.link)
            with open('database.pwp', 'w') as f:
                f.write('$'.join(donelist))
                f.close()
        time.sleep(900)
