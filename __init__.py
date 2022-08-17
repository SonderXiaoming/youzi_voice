import os
from nonebot import MessageSegment
from hoshino import Service, priv, R
from . import getvoiece
from .youdaotranslate import translate

sv_help = '''
【柚子中配】+ （角色id） + 文本
【柚子日配】+ （角色id） + 文本
不填默认为宁宁，加号省略
【柚子id列表】查看支持角色
'''.strip()

speaker_id = '''
0；綾地寧々
1；因幡めぐる
2；朝武芳乃
3；常陸茉子
4；ムラサメ
5；鞍馬小春
6；在原七海
'''.strip()

sv = Service(
    name='JapaneseTTS',  # 功能名
    use_priv=priv.NORMAL,  # 使用权限
    manage_priv=priv.ADMIN,  # 管理权限
    visible=True,  # False隐藏
    enable_on_default=True,  # 是否默认启用
    help_ = sv_help
)

@sv.on_prefix("柚子中配")
async def youzi_voice_cn(bot, ev):
    text = ev.message.extract_plain_text()
    content = text.split()
    voice_send = R.get('record', 'demo.wav') 
    path_wav = os.path.abspath(voice_send.path)
    if len(content) == 1:
        text_chjp = await getvoiece.chinese2katakana(content[0])
        A = getvoiece.getvoice()
    elif content[0].isdigit():
        text_chjp = await getvoiece.chinese2katakana(content[1])
        A = getvoiece.getvoice(int(content[0]))
    else:
        await bot.send(ev, sv_help)
        return
    await A.gethash(text_chjp)
    await A.getvoice(path_wav)
    final_send = MessageSegment.record(f'file:///{os.path.abspath(voice_send.path)}')
    await bot.send(ev, final_send)

@sv.on_prefix("柚子日配")
async def youzi_voice_ja(bot, ev):
    text = ev.message.extract_plain_text()
    content = text.split()
    voice_send = R.get('record', 'demo.wav') 
    path_wav = os.path.abspath(voice_send.path)
    if len(content) == 1:
        text_chjp = await translate(content[0])
        A = getvoiece.getvoice()
    elif content[0].isdigit():
        text_chjp = await translate(content[1])
        A = getvoiece.getvoice(int(content[0]))
    else:
        await bot.send(ev, sv_help)
        return
    await bot.send(ev, text_chjp)
    await A.gethash(text_chjp)
    await A.getvoice(path_wav)
    final_send = MessageSegment.record(f'file:///{os.path.abspath(voice_send.path)}')
    await bot.send(ev, final_send)

@sv.on_fullmatch("柚子id列表")
async def speaker_list(bot, ev):
    await bot.send(ev, speaker_id)
