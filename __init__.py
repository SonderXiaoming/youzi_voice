from hoshino import Service, priv
from nonebot import MessageSegment
from .create_img import image_draw
from .youdaotranslate import translate
from .getvoiece import voiceApi, GenshinAPI, XcwAPI, Error, chinese2katakana, getvoice

sv_help = '''
【柚子/常轨脱离/缘之空/美少女万华镜/galgame】【中配/日配】+ （角色id） + 文本
（中配将中文翻译为片假名，日配翻译为日语，日配会输出翻译内容供检查）
不填默id认为0，加号替换为空格
例：柚子日配 0 我爱宁宁 
柚子中配 我爱宁宁 
柚子日配 私は綾地寧々を愛している（应该是这样，日语不好）
特殊：
xcw日配+日语/中文（自动翻译）
xcw中配+中文
派蒙说中文+中文（更新到鹿野院平藏）
【角色id列表】查看支持角色和分类
'''.strip()

speaker_dict = {
    '柚子': ["綾地寧々", "因幡めぐる", "朝武芳乃", "常陸茉子", "ムラサメ", "鞍馬小春", "在原七海", "四季ナツメ", "明月栞那", "墨染希", "火打谷愛衣", "汐山涼音"],
    '常轨脱离': ["和泉妃愛", "常盤華乃", "錦あすみ", "鎌倉詩桜", "竜閑天梨", "和泉里", "新川広夢", "聖莉々子"],
    '缘之空': ["春日野穹", "天女目瑛", "依媛奈緒", "渚一葉"],
    '美少女万華鏡': ["蓮華", "篝ノ霧枝", "沢渡雫", "亜璃子", "灯露椎", "覡夕莉"],
    'galgame': ["鷹倉杏璃", "鷹倉杏鈴", "アペイリア", "倉科明日香", "ATRI", "アイラ", "新堂彩音", "姫野星奏", "小鞠ゆい", "聖代橋氷織", "有坂真白", "白咲美絵瑠", "二階堂真紅"]
}

XCW = ['xcw', '小仓唯', '镜华']

genshin = ['派蒙', '凯亚', '安柏', '丽莎', '琴', '香菱', '枫原万叶', '迪卢克', '温迪', '可莉', '早柚', '托马', '芭芭拉',
           '优菈', '云堇', '钟离', '魈', '凝光', '雷电将军', '北斗', '甘雨', '七七', '刻晴', '神里绫华', '雷泽', '神里绫人',
           '罗莎莉亚', '阿贝多', '八重神子', '宵宫', '荒泷一斗', '九条裟罗', '夜兰', '珊瑚宫心海', '五郎', '达达利亚', '莫娜',
           '班尼特', '申鹤', '行秋', '烟绯', '久岐忍', '辛焱', '砂糖', '胡桃', '重云', '菲谢尔', '诺艾尔', '迪奥娜', '鹿野院平藏']

speaker_id = '''
===========柚子=============
0：綾地寧々    1：因幡めぐる
2：朝武芳乃    3：常陸茉子
4：ムラサメ    5：鞍馬小春
6：在原七海    7：四季ナツメ
8：明月栞那    9：墨染希
10：火打谷愛衣 11：汐山涼音
=========常轨脱离===========
0：和泉妃愛    1：常盤華乃
2：錦あすみ    3：鎌倉詩桜
4：竜閑天梨    5：和泉里
6：新川広夢    7：聖莉々子
==========缘之空============
0：春日野穹    1：天女目瑛
2：依媛奈緒    3：渚一葉
=========美少女万華鏡========
0：蓮華        1：篝ノ霧枝
2：沢渡雫      3：亜璃子
4：灯露椎      5：覡夕莉
==========galgame===========
0：鷹倉杏璃    1：鷹倉杏鈴
2：アペイリア  3：倉科明日香
4：ATRI        5：アイラ
6：新堂彩音    7：姫野星奏
8：小鞠ゆい    9：聖代橋氷織
10：有坂真白   11：白咲美絵瑠
12：二階堂真紅
=========公主连结===========
特殊：xcw中配/日配
===========原神=============
特殊：xx中配
'''.strip()


def get_speakers(choose, num=0):
    if choose == '常轨脱离':
        speakers, model = speaker_dict["常轨脱离"][num], 5
    elif choose == '缘之空':
        speakers, model = speaker_dict["缘之空"][num], 13
    elif choose == '美少女万華鏡':
        speakers, model = speaker_dict["美少女万華鏡"][num], 17
    elif choose == "galgame":
        speakers, model = speaker_dict["galgame"][num], 29
    else:
        speakers = speaker_dict["柚子"][num]
        if num >= 7:
            model = 9
        else:
            model = 1
    return speakers, model


sv = Service(
    name='角色语音模仿',  # 功能名
    use_priv=priv.NORMAL,  # 使用权限
    manage_priv=priv.ADMIN,  # 管理权限
    visible=True,  # False隐藏
    enable_on_default=True,  # 是否默认启用
    help_=sv_help
)


@sv.on_prefix([i + '中配' for i in speaker_dict.keys()])
async def youzi_voice_cn(bot, ev):
    text = ev.raw_message
    content = text.split()
    if len(content) == 2:
        speaker, model = get_speakers(content[0][:-2])
        text_chjp = await chinese2katakana(content[1])
        A = getvoice(speaker, model)
    elif content[1].isdigit():
        speaker, model = get_speakers(content[0][:-2], int(content[1]))
        text_chjp = await chinese2katakana(content[2])
        A = getvoice(speaker, model)
    else:
        await bot.send(ev, sv_help)
        return
    try:
        voice = await A.gethash(text_chjp)
        final_send = MessageSegment.record(voice)
        await bot.send(ev, final_send)
    except:
        await bot.send(ev, "生成失败，红豆泥斯密马赛~")


@sv.on_prefix([i + '日配' for i in speaker_dict.keys()])
async def youzi_voice_ja(bot, ev):
    text = ev.raw_message
    content = text.split()
    if len(content) == 2:
        speaker, model = get_speakers(content[0][:-2])
        text_chjp = await translate(content[1])
        A = getvoice(speaker, model)
    elif content[1].isdigit():
        speaker, model = get_speakers(content[0][:-2], int(content[1]))
        text_chjp = await translate(content[2])
        A = getvoice(speaker, model)
    else:
        await bot.send(ev, sv_help)
        return
    await bot.send(ev, text_chjp)
    try:
        voice = await A.gethash(text_chjp)
        final_send = MessageSegment.record(voice)
        await bot.send(ev, final_send)
    except:
        await bot.send(ev, "生成失败，红豆泥斯密马赛~")


@sv.on_prefix([i + '日配' for i in XCW])
@sv.on_prefix([i + '中配' for i in genshin])
@sv.on_prefix([i + '中配' for i in XCW])
async def voice(bot, ev):
    try:
        text: str = ev.message.extract_plain_text().strip()
        if not text:
            await bot.send(ev, '请输入需要合成语音的文本', at_sender=True)
            return
        preid: str = ev.prefix[:-3]
        prelang: str = ev.prefix[-2:]
        if prelang == '中文':
            if preid in XCW:
                text = await chinese2katakana(text)
                voice = await voiceApi(XcwAPI + text)
            else:
                voice = await voiceApi(GenshinAPI, {'speaker': preid, 'text': text, 'length': 1.0})
        else:
            text = await translate(text)
            voice = await voiceApi(XcwAPI + text)
        data = MessageSegment.record(voice)
    except Error as e:
        data = f'发生错误：{e.error}'
        sv.logger.error(data)
    except Exception as e:
        data = f'发生错误：{e}'
        sv.logger.error(data)
    await bot.send(ev, data)


@sv.on_fullmatch("角色id列表")
async def speaker_list(bot, ev):
    img = image_draw(speaker_id)
    await bot.send(ev, f'[CQ:image,file={img}]')
