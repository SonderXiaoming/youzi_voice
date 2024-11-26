import json
from lxml import etree
import base64
import httpx
import random
import asyncio
from string import ascii_lowercase, digits

ALPHABET = ascii_lowercase + digits

COOKIES = {
    "__gads": "ID=0913d7b7838088a9-22d4a86186d500c8:T=1660228904:RT=1660228904:S=ALNI_MYLAxIRws8hObfvoeF5wkg6F8_1qg",
    "__gpi": "UID=00000880c2f1ffa9:T=1660228904:RT=1660228904:S=ALNI_ManV7rXnEUgMAuUxsLEFkSYonxQRQ",
    "__utmc": "79062217",
    "__utmz": "79062217.1660228909.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)",
    "__utmt": "1",
    "__utma": "79062217.169553450.1660228904.1660228904.1660228904.1",
    "__utmb": "79062217.4.10.1660228909",
}

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Origin": "https://www.ltool.net",
    "Referer": "https://www.ltool.net/chinese-simplified-and-traditional-characters-pinyin-to-katakana-converter-in-simplified-chinese.php",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.47",
    "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
}


def local_hash():
    return "".join(random.choice(ALPHABET) for _ in range(10))


async def chinese2katakana(text):

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://www.ltool.net/chinese-simplified-and-traditional-characters-pinyin-to-katakana-converter-in-simplified-chinese.php",
            headers=HEADERS,
            data={
                "contents": f"{text}",
                "firstinput": "OK",
                "option": "1",
                "optionext": "zenkaku",
            },
            cookies=COOKIES,
        )
        a = resp.text
    return "".join(etree.HTML(a).xpath("/html//form/div[5]/div/text()"))


class MOETTSVoice:
    def __init__(self, speaker: str, fn_num: int, trigger_id: int = 17):
        self.speaker = speaker
        self.num = fn_num
        self.trigger_id = trigger_id

    async def get_voice(self, text):
        async with httpx.AsyncClient() as client:
            hash = local_hash()
            await client.post(
                "https://skytnt-moe-tts.hf.space/queue/join?__theme=light",
                json={
                    "fn_index": self.num,
                    "data": [text, self.speaker, 1, False],
                    "session_hash": hash,
                    "event_data": None,
                    "trigger_id": self.trigger_id,
                },
            )

            async with client.stream(
                "GET", f"https://skytnt-moe-tts.hf.space/queue/data?session_hash={hash}"
            ) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    if line:
                        if line.startswith("data: "):
                            data_str = line.replace("data: ", "")
                            event_data: dict = json.loads(data_str)

                            msg = event_data.get("msg")
                            if msg == "process_completed":
                                data_url = event_data["output"]["data"][1]["url"]
                                break

            data = await client.get(data_url)
            return "base64://" + base64.b64encode(data.content).decode()


if __name__ == "__main__":
    A = MOETTSVoice("綾地寧々", 0, 17)
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(A.get_voice("こんにちは。"))
    print(result)
