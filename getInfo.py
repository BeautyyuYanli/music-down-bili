import requests, json, re, time
from multiprocessing import Process, Queue
import Bv2Av
q = Queue()
fid = 1117924884
num_max = 10


class List(Process):
    def __init__(self, url, q):
        super(List, self).__init__()
        self.url = url
        self.q = q
        self.headers = {
            'Referer': 'https://space.bilibili.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }
    def run(self):
        self.getList()
    def send_request(self,url):
        i = 0
        while i < 3:
            try:
                return json.loads(requests.get(url, headers=self.headers).text)
            except:
                i += 1
    def getList(self):
        res = self.send_request(self.url)
        pn = re.findall(r'(?<=pn=)[0-9]*',self.url)[0]
        elements = ['title', 'cover', 'bvid']
        try:
            len_vedios = len(res['data']['medias'])
            for j in range(len_vedios):
                vedio = {}
                for k in elements:
                    vedio[k] = res['data']['medias'][j][k]
                vedio['link'] = Bv2Av.bv2av(vedio['bvid'])
                vedio['pn'] = pn
                # print(vedio,'\n')
                self.q.put(vedio)
                # print(q.get())
        except:return

def takePn(elem):
    return elem['pn']

def get_list(fid,num_max):
    list = []
    url_list = ['https://api.bilibili.com/x/v3/fav/resource/list?media_id=' + str(fid) + '&pn=' + str(num) + '&ps=20&keyword=&order=mtime&type=0&tid=0&platform=web&amp;jsonp=jsonp' for num in range(1,num_max+1)]
    Process_list = []
    for url in url_list:
        p = List(url, q)
        p.start()
        Process_list.append(p)
    for i in Process_list:
        i.join()
    while not q.empty():
        list.append(q.get())
    list.sort(key = takePn)
    return list

if __name__ == '__main__':
    start_time = time.time()
    list = get_list(fid ,num_max)
    # with open('database.pwp', 'r') as f:
    #     donelist = f.read().split('$')
    with open('database.qwq','w') as f:
        f.write(str(list))
