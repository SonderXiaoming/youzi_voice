import random
import requests
from lxml import etree
import base64
import json
import re

speaker_list = ["綾地寧々","因幡めぐる","朝武芳乃","常陸茉子","ムラサメ","鞍馬小春","在原七海"]

def local_hash():
    alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'
    a = ""
    for it in range(10):
        char = random.choice(alphabet)
        a = a+char
    return a

def chinese2katakana(text):
    #text = parse.quote(text)
    print(text)
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

def chinese2japanese(text,language='ja'):
    
    url = 'https://translate.google.cn/_/TranslateWebserverUi/data/batchexecute?rpcids=MkEWBc&f.sid=-2984828793698248690&bl=boq_translate-webserver_20201221.17_p0&hl=zh-CN&soc-app=1&soc-platform=1&soc-device=1&_reqid=5445720&rt=c'
    headers = {
	    'origin': 'https://translate.google.cn',
	    'referer': 'https://translate.google.cn/',
	    'sec-fetch-dest': 'empty',
	    'sec-fetch-mode': 'cors',
	    'sec-fetch-site': 'same-origin',
	    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36',
	    'x-client-data': 'CIW2yQEIpbbJAQjEtskBCKmdygEIrMfKAQj2x8oBCPfHygEItMvKAQihz8oBCNzVygEIi5nLAQjBnMsB',
	    'Decoded':'message ClientVariations {repeated int32 variation_id = [3300101, 3300133, 3300164, 3313321, 3318700, 3318774, 3318775, 3319220, 3319713, 3320540, 3329163, 3329601];}',
	    'x-same-domain': '1'
	    }  
    data = {
        	'f.req': f'[[["MkEWBc","[[\\"{text}\\",\\"auto\\",\\"{language}\\",true],[null]]",null,"generic"]]]'
    	}  
    
    res = requests.post(url, headers=headers, data=data).text
    pattern = '\)\]\}\'\s*\d{3,4}\s*\[(.*)\s*' 
    part1 = re.findall(pattern, res)
    part1_list = json.loads('['+part1[0])[0]
    if part1_list[2] is None:  
        return text
    content1 = part1_list[2].replace('\n', '')
    part2_list = json.loads(content1)[1][0][0][5:][0]
    s = ''
    for i in part2_list:  
        s += i[0]
        # s += i[1][1] 
    return s

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
        
    def gethash(self,text):
        self.json_data = {
            'fn_index': 0,
            'data': [
                f'{text}',
                f'{self.speaker}',
            ],
            'action': 'predict',
            'session_hash': f'{self.hash}',
        }

        response = requests.post('https://hf.space/embed/skytnt/moe-japanese-tts/api/queue/push/', headers=self.headers, json=self.json_data)
        self.voicehash = response.json().get("hash")
        print(self.voicehash)
        
    def getvoice(self,path):
        self.path = path
        self.json_data_2 = {
            'hash': f'{self.voicehash}',
        }
        self.json_data_2 = str(self.json_data_2)
        self.json_data_2 = self.json_data_2.replace("'",'"').replace(" ","")
        self.json_data_2 = self.json_data_2.encode()
        response = requests.post('https://hf.space/embed/skytnt/moe-japanese-tts/api/queue/status/', headers=self.headers, data=self.json_data_2)
        a = response.json()
        if a.get('status') == 'PENDING' or a.get('status') == 'QUEUED':
            getvoice.getvoice(self,self.path)
            return
        voice_base64 = a.get("data").get("data")[1].split(",")[1]
        voice_b = base64.b64decode(voice_base64)
        with open(f"{path}","wb") as f:
            f.write(voice_b)