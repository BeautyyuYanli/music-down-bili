import requests, ffmpeg, time, re, codecs
from modules import downloader, metadata, getInfo
from production import config

if __name__ == '__main__':
    list = getInfo.get_list(config.fid, config.num_max)
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
            video_title = downloader.main(i['link'] + '?p=1', './bilibili_video')
            video_path = './bilibili_video/' + video_title + '/' + video_title + '.flv'
            # convert into audio
            audio_path = 'output/' + \
                re.sub(r'[\/\\:*?"<>|]', '', i['title']) + '.mp3'
            ffmpeg.input(video_path).output(audio_path, ab='1080k').run()
            # insert cover
            try:
                metadata.addTag(audio_path, title=i['title'], cover=requests.get(i['cover']).content, album=i['title'])
            except:
                with open('./production/log.txt', 'a') as f:
                    f.writelines(
                        'error when inserting tag to: ' + i['title'] + i['link'])
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
