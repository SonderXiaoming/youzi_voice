import os
from pyexpat import model
from nonebot import MessageSegment
from hoshino import Service, priv, R
from . import getvoiece
from .youdaotranslate import translate

sv_help = '''
【柚子/常轨脱离/缘之空】【中配/日配】+ （角色id） + 文本
（中配将中文翻译为片假名，日配翻译为日语，日配会输出翻译内容供检查）
【柚子/常轨脱离/缘之空】【纯日配】+ （角色id） + 文本
（给日语N114514水平的人准备，不翻译，但要求用户直接输入日语）
不填默id认为0，加号替换为空格
例：柚子日配 0 我爱宁宁 
柚子中配 我爱宁宁 
柚子纯日配 私は綾地寧々を愛している（应该是这样，日语不好）
【角色id列表】查看支持角色和分类
'''.strip()

speaker_dict = {
'柚子':["綾地寧々","因幡めぐる","朝武芳乃","常陸茉子","ムラサメ","鞍馬小春","在原七海","四季ナツメ","明月栞那","墨染希","火打谷愛衣","汐山涼音"],
'常轨脱离':["和泉妃愛","常盤華乃","錦あすみ","鎌倉詩桜","竜閑天梨","和泉里","新川広夢","聖莉々子"],
'缘之空':["春日野穹","天女目瑛","依媛奈緒","渚一葉"],
}

speaker_id = '''
=====柚子=====
0；綾地寧々
1；因幡めぐる
2；朝武芳乃
3；常陸茉子
4；ムラサメ
5；鞍馬小春
6；在原七海
7；"四季ナツメ"
8；"明月栞那"
9；"墨染希"
10；"火打谷愛衣"
11；"汐山涼音"
====常轨脱离====
0；"和泉妃愛"
1；"常盤華乃"
2；"錦あすみ"
3；"鎌倉詩桜"
4；"竜閑天梨"
5；"和泉里"
6；"新川広夢"
7；"聖莉々子"
====缘之空=====
0；"春日野穹"
1；"天女目瑛"
2；"依媛奈緒"
3；"渚一葉"
'''.strip()

voice_send = R.get('record', 'demo.wav') 
path_wav = os.path.abspath(voice_send.path)

def get_speakers(choose,num=0):
    if choose == '常轨脱离':
        speakers,model = speaker_dict["常轨脱离"][num],1
    elif choose == '缘之空':
        speakers,model = speaker_dict["缘之空"][num],3
    else:
        speakers = speaker_dict["柚子"][num]
        if num>=7:
            model = 2
        else:
            model = 0
    return speakers,model

path = os.path.abspath(R.get('record').path)
if not os.path.exists(path):
    os.makedirs(path)#校验文件

sv = Service(
    name='JapaneseTTS',  # 功能名
    use_priv=priv.NORMAL,  # 使用权限
    manage_priv=priv.ADMIN,  # 管理权限
    visible=True,  # False隐藏
    enable_on_default=True,  # 是否默认启用
    help_ = sv_help
)

@sv.on_prefix("柚子中配",'常轨脱离中配','缘之空中配')
async def youzi_voice_cn(bot, ev):
    text = ev.raw_message
    content = text.split()
    if len(content) == 2:
        speaker,model = get_speakers(content[0][:-2])
        text_chjp = await getvoiece.chinese2katakana(content[1])
        A = getvoiece.getvoice(speaker,model)
    elif content[1].isdigit():
        speaker,model = get_speakers(content[0][:-2],int(content[1]))
        text_chjp = await getvoiece.chinese2katakana(content[2])
        A = getvoiece.getvoice(speaker,model)
    else:
        await bot.send(ev, sv_help)
        return
    await A.gethash(text_chjp)
    await A.getvoice(path_wav)
    final_send = MessageSegment.record(f'file:///{os.path.abspath(voice_send.path)}')
    await bot.send(ev, final_send)

@sv.on_prefix("柚子日配",'常轨脱离日配','缘之空日配')
async def youzi_voice_ja(bot, ev):
    text = ev.raw_message
    content = text.split()
    if len(content) == 2:
        speaker,model = get_speakers(content[0][:-2])
        text_chjp = await translate(content[1])
        A = getvoiece.getvoice(speaker,model)
    elif content[1].isdigit():
        speaker,model = get_speakers(content[0][:-2],int(content[1]))
        text_chjp = await translate(content[2])
        A = getvoiece.getvoice(speaker,model)
    else:
        await bot.send(ev, sv_help)
        return
    await bot.send(ev, text_chjp)
    await A.gethash(text_chjp)
    await A.getvoice(path_wav)
    final_send = MessageSegment.record(f'file:///{os.path.abspath(voice_send.path)}')
    await bot.send(ev, final_send)

@sv.on_prefix("柚子纯日配",'常轨脱离纯日配','缘之空纯日配')
async def youzi_focus_ja(bot, ev):
    text = ev.raw_message
    content = text.split()
    if len(content) == 2:
        speaker,model = get_speakers(content[0][:-2])
        text_chjp = content[1]
        A = getvoiece.getvoice(speaker,model)
    elif content[1].isdigit():
        speaker,model = get_speakers(content[0][:-2],int(content[1]))
        text_chjp = content[2]
        A = getvoiece.getvoice(speaker,model)
    else:
        await bot.send(ev, sv_help)
        return
    await A.gethash(text_chjp)
    await A.getvoice(path_wav)
    final_send = MessageSegment.record(f'file:///{os.path.abspath(voice_send.path)}')
    await bot.send(ev, final_send)

@sv.on_fullmatch("角色id列表")
async def speaker_list(bot, ev):
    await bot.send(ev, speaker_id)
