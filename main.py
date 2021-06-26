import requests, ffmpeg, time, re, codecs
from modules import downloader, cover, getInfo
import production.config as config

if __name__ == '__main__':
    fid = re.findall(r'(?<=fid=)[0-9]*', config.url)[0]
    list = getInfo.get_list(fid, config.num_max)
    # prepare historylist
    with open('./production/history.list', 'r') as f:
        donelist = f.read().split('\n')
    # check update
    update_pool = []
    for i in list:
        if i['link'] not in donelist:
            print(i['link'])
            update_pool.append(i)
    # update
    print('\ndownloading start\n')
    for i in update_pool:
        try:
            # download video
            ftitle = downloader.main(i['link'] + '?p=1')
            # convert into audio
            mp3path = 'output/' + \
                re.sub(r'[\/\\:*?"<>|]', '', i['title']) + '.mp3'
            {ffmpeg
                .input('bilibili_video/' + ftitle + '/' + ftitle + '.flv')
                .output(mp3path, ab='1080k')
                .run()
             }
            # insert cover
            try:
                cover.add_cover(cover.get_cover(i['cover']), mp3path)
            except:
                with open('./production/log.txt', 'a') as f:
                    f.writelines(
                        'error when inserting cover to: ' + ftitle + i['link'])
        except:
            with open('./production/log.txt', 'a') as f:
                f.writelines('error when downloading: ' + i['link'], '\n')
        else:
            print('successfully downloaded: ' + i['link'])
            # update database
            donelist.append(i['link'])
            with open('./production/history.list', 'w') as f:
                f.write('\n'.join(donelist))
                f.close()
        time.sleep(config.delayTime)
