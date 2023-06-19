# 爬取图片(二进制数据)，将二进制数据保存到jpg文件中，这样图片就可以保存下来了

# 成功

import requests

url = 'https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fsafe-img.xhscdn.com%2Fbw1%2F541ccb1f-0020-48f4-8413-5b4bf7f8cc76%3FimageView2%2F2%2Fw%2F1080%2Fformat%2Fjpg&refer=http%3A%2F%2Fsafe-img.xhscdn.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1687310023&t=a19c6740752b9de81360e2198e86d22c'

response = requests.get(url)

# print(response.content)

with open('liuyifei-huamulan.jpg','wb')as f:
    f.write(response.content)