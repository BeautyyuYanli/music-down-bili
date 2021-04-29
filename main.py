import requests, ffmpeg, time, re, codecs
import downloader, cover, getInfo
# config
url = 'https://space.bilibili.com/438584984/favlist?fid=1117924884&ftype=create'
num_max = 10

if __name__ == '__main__':
    st = time.time()
    fid = re.findall(r'(?<=fid=)[0-9]*',url)[0]
    list = getInfo.get_list(fid,num_max)
    # prepare database
    with open('database.pwp', 'r') as f:
        donelist = f.read().split('$')
    # check update
    update_pool = []
    for i in list:
        if i['link'] not in donelist :
            print(i['link'])
            update_pool.append(i)
    print(time.time()-st)
# update
    print('\ndownloading start\n')
    for i in update_pool:
        try:
            # download video
            ftitle = downloader.main(i['link'] + '?p=1')
            # convert into audio
            mp3path = 'output/' + re.sub(r'[\/\\:*?"<>|]', '', i['title']) + '.mp3'
            {ffmpeg
                .input('bilibili_video/' + ftitle + '/' + ftitle + '.flv')
                .output(mp3path, ab = '1080k')
                .run()
            }
            # insert cover
            try:
                cover.add_cover(cover.get_cover(i['cover']), mp3path)
            except:
                with open('./log.txt', 'a') as f:
                    f.writelines('error when inserting cover to: ' + ftitle + i['link'])
        except:
            with open('./log.txt', 'a') as f:
                f.writelines('error when downloading: ' + i['link'],'\n')
        else:
            print('successfully downloaded: ' + i['link'])
            # update database
            donelist.append(i['link'])
            with open('database.pwp', 'w') as f:
                f.write('$'.join(donelist))
                f.close()
        time.sleep(900)
