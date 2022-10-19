import base64

# 图片转换成base64
import re


def image_to_base64(path):
    with open(path, 'rb') as img:
        # 使用base64进行编码
        b64encode = base64.b64encode(img.read())
        s = b64encode.decode()
        b64_encode = 'data:image/jpeg;base64,%s' % s
        # 返回base64编码字符串
        return b64_encode


# print(image_to_base64("badMouse.png"))

url = "https://space.bilibili.com/8020359?spm_id_from=444.41.0.0"
url2 = "https://space.bilibili.com/473500883/video?tid=0&page=2&keyword=&order=pubdate"
url3 = "https://www.douyin.com/user/MS4wLjABAAAAUwyh5pntLvnqzRRO5j9Y9etaoYmTf0O3R0y3tpLB4nBElLNMbDY-0zERKF2p0o-2?vid=7134558532518579471"
print(re.search('\d+$', url3).group())
