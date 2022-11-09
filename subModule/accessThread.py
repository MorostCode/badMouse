from PyQt5.QtCore import QThread, pyqtSignal
from urllib import parse
import requests
import datetime
import math
import json
import os
import re


class AccessThread(QThread):
    # 声明一个信号
    update_signal = pyqtSignal(str)

    def __init__(self, url):
        super(AccessThread, self).__init__()
        self.url = url
        self.cwd = os.getcwd()  # 记录当前工作目录
        self.count = 0
        self.name = None
        self.headers = {
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
            }

    def run(self):
        try:
            # 判断域名
            domainName = self.url.split("https://")[-1].split(".com")[0]
            if domainName == "www.douyin":
                sec_user_id = parse.urlparse(self.url).path.split("user/")[-1]
                api_url = "https://www.douyin.com/aweme/v1/web/aweme/post/?device_platform=webapp&aid=6383&sec_user_id=" + sec_user_id + "&max_cursor=0"
                print("111")
                self.access_dy(api_url)
                self.name = None  # 每次爬取后重置命名

            elif domainName == "space.bilibili":
                uid = re.search("\d+", self.url).group()  # 正则匹配获取用户id
                api_url = "https://api.bilibili.com/x/space/arc/search?mid=" + uid + "&ps=30&tid=0&pn=1&keyword=&order=pubdate&order_avoided=true&jsonp=jsonp"
                self.access_bili(api_url)
                self.name = None  # 每次爬取后重置命名
        except Exception as e:
            error_line = e.__traceback__.tb_lineno
            error_info = '第{error_line}行发生error为: {e}'.format(error_line=error_line, e=str(e))
            print(error_info)

    # 访问抖音api获取Url列表
    def access_dy(self, url):
        try:
            max_cursor = 0
            # 只要hasmore是否为true，则反复访问作者主页链接，直到成功返回这个为false
            while True:
                # 替换url中max_cursor的值
                url_parsed = parse.urlparse(url)
                bits = list(url_parsed)
                qs = parse.parse_qs(bits[4])
                qs['max_cursor'] = max_cursor
                bits[4] = parse.urlencode(qs, True)
                url = parse.urlunparse(bits)
                # 请求接口，解析结果
                headers = self.headers
                headers['referer'] = self.url
                r = requests.get(url=url, headers=headers, stream=True)
                data_json = json.loads(r.text)
                print(data_json)
                if len(data_json['aweme_list']) == 0:
                    break
                # 获取用户名称，以此命名txt文件
                if not self.name:
                    self.name = data_json['aweme_list'][0]['author']['nickname']
                # 打开txt文件保存数据
                time_now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
                with open(os.path.join(self.cwd, "{}_{}.txt".format(self.name, time_now)), "a", encoding="utf-8") as f:
                    for i in range(len(data_json['aweme_list'])):
                        title = data_json['aweme_list'][i]['desc']
                        link = data_json['aweme_list'][i]['video']['play_addr']['url_list'][0]
                        f.write(title + "\n")
                        f.write(link + "\n\n")
                        self.count += 1
                # 每次重置这个页数，继续替换url中下一页页码进行访问
                max_cursor = data_json['max_cursor']
                has_more = data_json['has_more']
                if has_more is False:
                    break
            # 发送信号，成功爬取的数据总数
            self.update_signal.emit((str(self.count)))
            self.count = 0
        except Exception as e:
            error_line = e.__traceback__.tb_lineno
            error_info = '第{error_line}行发生error为: {e}'.format(error_line=error_line, e=str(e))
            print(error_info)

    # 访问B站api获取BV列表
    def access_bili(self, url):
        try:
            r = requests.get(url=url, headers=self.headers, stream=True)
            data_json = json.loads(r.text)
            pageNum = math.ceil(data_json['data']['page']['count'] / data_json['data']['page']['ps'])
            for num in range(pageNum):
                url_parsed = parse.urlparse(url)
                bits = list(url_parsed)
                qs = parse.parse_qs(bits[4])
                qs['pn'] = str(num + 1)
                bits[4] = parse.urlencode(qs, True)
                url = parse.urlunparse(bits)
                # 请求接口，解析结果
                r = requests.get(url=url, headers=self.headers, stream=True)
                data_json = json.loads(r.text)
                if len(data_json['data']['list']['vlist']) == 0:
                    break
                # 获取用户名称，以此命名txt文件
                if not self.name:
                    self.name = data_json['data']['list']['vlist'][0]['author']
                # 打开txt文件保存数据
                time_now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
                with open(os.path.join(self.cwd, "{}_{}.txt".format(self.name, time_now)), "a", encoding="utf-8") as f:
                    for i in range(len(data_json['data']['list']['vlist'])):
                        title = data_json['data']['list']['vlist'][i]['title']
                        bvid = data_json['data']['list']['vlist'][i]['bvid']
                        f.write(title + "\n")
                        f.write(bvid + "\n\n")
                        self.count += 1
            # 发送信号，成功爬取的数据总数
            self.update_signal.emit((str(self.count)))
            self.count = 0
        except Exception as e:
            error_line = e.__traceback__.tb_lineno
            error_info = '第{error_line}行发生error为: {e}'.format(error_line=error_line, e=str(e))
            print(error_info)

