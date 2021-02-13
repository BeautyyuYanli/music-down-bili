# music-down-bili

本项目的功能是 下载一个b站收藏夹中的视频并转为音频. 本项目尚且处于非常简陋的阶段.

## 使用

参照[使用rsshub订阅bilibili收藏夹](https://docs.rsshub.app/social-media.html#bilibili-up-zhu-fei-mo-ren-shou-cang-jia), 用相应的rss链接替换掉`main.py` 中的`rssurl`

运行`python main.py` 即可在`output` 文件夹中获得相应的音频文件.

## 引用

- 本项目使用了[rsshub](https://github.com/DIYgod/RSSHub)
- 本项目使用了[Bilibili_video_download](https://github.com/Henryhaohao/Bilibili_video_download)的代码