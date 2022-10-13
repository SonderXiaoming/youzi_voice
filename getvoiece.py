import json
from aiowebsocket.converses import AioWebSocket
from lxml import etree
import base64
import aiohttp
from typing import Union

GenshinAPI = 'http://233366.proxy.nscc-gz.cn:8888'
XcwAPI = 'http://prts.tencentbot.top/0/'

def local_hash():
    alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'
    a = ""
    for it in range(10):
        char = random.choice(alphabet)
        a = a+char
    return a

async def chinese2katakana(text):
    cookies = {
        '__gads': 'ID=0913d7b7838088a9-22d4a86186d500c8:T=1660228904:RT=1660228904:S=ALNI_MYLAxIRws8hObfvoeF5wkg6F8_1qg',
        '__gpi': 'UID=00000880c2f1ffa9:T=1660228904:RT=1660228904:S=ALNI_ManV7rXnEUgMAuUxsLEFkSYonxQRQ',
        '__utmc': '79062217',
        '__utmz': '79062217.1660228909.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
        '__utmt': '1',
        '__utma': '79062217.169553450.1660228904.1660228904.1660228904.1',
        '__utmb': '79062217.4.10.1660228909',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Origin': 'https://www.ltool.net',
        'Referer': 'https://www.ltool.net/chinese-simplified-and-traditional-characters-pinyin-to-katakana-converter-in-simplified-chinese.php',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.47',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    data = {
        'contents': f'{text}',
        'firstinput': 'OK',
        'option': '1',
        'optionext': 'zenkaku',
    }
    async with aiohttp.ClientSession() as session: 
        async with session.post('https://www.ltool.net/chinese-simplified-and-traditional-characters-pinyin-to-katakana-converter-in-simplified-chinese.php', headers=headers, data=data, cookies=cookies) as resp:
            a = await resp.text()
    html = etree.HTML(a)
    text = html.xpath("/html//form/div[5]/div/text()")
    text_full = ""
    for it in text:
        text_full = text_full + it
    print(text_full)
    return text_full

class getvoice(object):
    def __init__(self,speaker,num) :
        self.speaker = speaker
        self.num = num
        self.count = 0
        
    async def gethash(self,text):
        uri = 'wss://spaces.huggingface.tech/skytnt/moe-tts/queue/join'
        async with AioWebSocket(uri) as aws:
            converse = aws.manipulator
            while True:
                receive = await converse.receive()
                print(receive.decode())
                a = json.loads(receive.decode())
                if a["msg"] == "send_data":
                    if self.count == 0:
                        message = {"fn_index":self.num,"data":[text,self.speaker,1,False],"session_hash":local_hash()}
                        message = str(message)
                        message = message.replace(" ","")
                        message = message.replace("'",'"')
                        message = message.replace("False",'false')
                        print(message)
                        await converse.send(message)
                    self.count = 1
                if a["msg"] == "process_completed":
                    self.count = 0
                    self.voicehash = a["output"]["data"][1]["name"]
                    break
        async with aiohttp.ClientSession() as session: 
            async with session.get(f'https://hf.space/embed/skytnt/moe-tts/file={self.voicehash}') as resp:
                a = await resp.content.read()
        return 'base64://' + base64.b64encode(a).decode()

async def voiceApi(api: str, params: Union[str, dict] = None) -> str:
    async with aiohttp.request('GET', api, params=params) as resp:
        if resp.status == 200:
            data = await resp.read()
        else:
            raise Error(resp.status)
    return 'base64://' + base64.b64encode(data).decode()

class Error(Exception):
    def __init__(self, args: object) -> None:
        self.error = args

