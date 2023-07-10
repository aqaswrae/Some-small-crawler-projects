#success
#https://www.virustotal.com/gui/home/search
#这个项目应该是不太行了，打断点时会报错，导致断点无法打上.ok了

#请求头中的x-vt-anti-abuse-header字段是经过js生成的

#打开上方的网址后搜索的是python

import requests,random,base64

#按照js代码的逻辑编写
def get_base64_str():
  e = '-ZG9udCBiZSBldmls-' + str(int(10000000000 * (1 + random.random() % 50000)))
  byte_data = e.encode('utf-8')
  final_data = base64.b64encode(byte_data).decode('utf-8')#转成base64编码
  return final_data

base64_str = get_base64_str()

url = "https://www.virustotal.com/ui/search?limit=20&relationships%5Bcomment%5D=author%2Citem&query=python"

payload = {}
headers = {
  'authority': 'www.virustotal.com',
  'accept': 'application/json',
  'accept-ianguage': 'en-US,en;q=0.9,es;q=0.8',
  'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
  'content-type': 'application/json',
  'cookie': '_gid=GA1.2.202099671.1687182065; _ga=GA1.2.581288611.1687182063; _ga_BLNDV9X2JR=GS1.1.1687182062.1.1.1687182222.0.0.0; _gat=1',
  'referer': 'https://www.virustotal.com/',
  'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
  'x-app-version': 'v1x187x3',
  'x-tool': 'vt-ui-main',
  'x-vt-anti-abuse-header': base64_str
}

response = requests.get(url,headers=headers)

print(response.text)

