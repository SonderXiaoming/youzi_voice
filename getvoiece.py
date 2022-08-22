import random
import requests
import asyncio
from lxml import etree
import base64
import aiohttp
import wave
import json

speaker_list = ["model0/綾地寧々","model0/因幡めぐる","model0/朝武芳乃","model0/常陸茉子","model0/ムラサメ","model0/鞍馬小春","model0/在原七海"]

async def local_hash():
    alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'
    a = ""
    for it in range(10):
        char = random.choice(alphabet)
        a = a+char
    return a

async def chinese2katakana(text):
    #text = parse.quote(text)
    #print(text)
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

    response = requests.post('https://www.ltool.net/chinese-simplified-and-traditional-characters-pinyin-to-katakana-converter-in-simplified-chinese.php', cookies=cookies, headers=headers, data=data)
    #print(response.text)
    html = etree.HTML(response.text)
    text = html.xpath("/html//form/div[5]/div/text()")
    text_full = ""
    for it in text:
        text_full = text_full + it
    return text_full

class getvoice(object):
    def __init__(self,speaker_id=0) :
        self.headers = {
            'authority': 'hf.space',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            # Already added when you pass json=
            # 'content-type': 'application/json',
            'origin': 'https://hf.space',
            'referer': 'https://hf.space/embed/skytnt/moe-japanese-tts/+?__theme=light',
            'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.47',
        }
        self.speaker = speaker_list[speaker_id]
        self.hash = local_hash()
        
    async def gethash(self,text):
        self.text = text
        self.json_data = {
            'fn_index': 0,
            'data': [
                f'{text}',
                f'{self.speaker}',
            ],
            'action': 'predict',
            'session_hash': f'{self.hash}',
        }
        async with aiohttp.ClientSession() as session: 
            async with session.post('https://hf.space/embed/skytnt/moe-japanese-tts/api/queue/push/', headers=self.headers, json=self.json_data) as resp:
                #self.voicehash = await resp.json()["hash"]
                a = await resp.json()
                self.voicehash = a.get("hash")
        #print(self.voicehash)
        
    async def getvoice(self,path):
        self.path = path
        self.json_data_2 = {
            'hash': f'{self.voicehash}',
        }
        
        async with aiohttp.ClientSession() as session: 
            async with session.post('https://hf.space/embed/skytnt/moe-japanese-tts/api/queue/status/', headers=self.headers,json=self.json_data_2) as resp:
                a =await resp.json()
                #print(a)  #######注释
        if a.get('status') == 'PENDING' or a.get('status') == 'QUEUED':
            await getvoice.getvoice(self,self.path)
            return
        if a.get("data").get("data")[1] == None :
            print(114514)  ######
            await getvoice.mixit(self,self.text)
            return
        voice_base64 = a.get("data").get("data")[1].split(",")[1]
        voice_b = base64.b64decode(voice_base64)
        with open(f"{path}","wb") as f:
            f.write(voice_b)
            
    async def mixit(self,text): #长度过长则混合合成
        gap = int(len(text)/2)
        text1 = text[:gap]
        text2 = text[gap:]
        path1 = self.path
        path2 = self.path+"1.wav"
        await getvoice.gethash(self,text1)
        await getvoice.getvoice(self,path1)
        await getvoice.gethash(self,text2)
        await getvoice.getvoice(self,path2)
        #########语言合成开始##########
        infiles = [path1, path2]
        outfile = path1
        data= []
        for infile in infiles:
            w = wave.open(infile, 'rb')
            data.append( [w.getparams(), w.readframes(w.getnframes())] )
            w.close()
        output = wave.open(outfile, 'wb')
        output.setparams(data[0][0])
        output.writeframes(data[0][1])
        output.writeframes(data[1][1])
        output.close()
            
        
        
        
        
if __name__ == "__main__":
    text = "车子千万不要外借！我真是吃了大亏了！朋友找我借车，碍于面子不好意思不借，结果昨天在路上遇见了，一点都不爱惜我的车，上坡还站起来蹬车，链子都掉了！气死我了！幸好今天是肯德基疯狂星期四，有人请我吃我感觉会好点"
    path = "demo.wav"
    text_chjp = asyncio.run(chinese2katakana(text))
    print(text_chjp)
    A = getvoice()
    A.gethash(text_chjp)
    A.getvoice(path)
    
