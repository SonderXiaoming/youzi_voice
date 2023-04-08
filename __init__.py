from hoshino import Service, priv
from nonebot import MessageSegment
from .create_img import image_draw
from .youdaotranslate import translate
from .getvoiece import voiceApi, GenshinAPI, XcwAPI, Error, chinese2katakana, getvoice
from PIL import Image, ImageDraw, ImageFont
import os
sv_help = '''
【柚子/常轨脱离/缘之空/美少女万华镜/galgame/零之使魔/TOLOVE】【中配/日配】+ （角色id） + 文本
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
    '柚子': 
    ["綾地寧々", "因幡めぐる", "朝武芳乃", "常陸茉子", "ムラサメ", "鞍馬小春", "在原七海", 
    "四季ナツメ", "明月栞那", "墨染希", "火打谷愛衣", "汐山涼音"
    "矢来美羽","布良梓","エリナ","稲村莉音","ニコラ","荒神小夜","大房ひよ里","淡路萌香","アンナ","倉端直太","枡形兵馬","扇元樹"],

    '常轨脱离': 
    ["和泉妃愛", "常盤華乃", "錦あすみ", "鎌倉詩桜", "竜閑天梨", "和泉里", "新川広夢", "聖莉々子"],

    '缘之空': 
    ["春日野穹", "天女目瑛", "依媛奈緒", "渚一葉"],

    '美少女万華鏡': 
    ["蓮華", "篝ノ霧枝", "沢渡雫", "亜璃子", "灯露椎", "覡夕莉"],

    'galgame': 
    ["鷹倉杏璃", "鷹倉杏鈴", "アペイリア", "倉科明日香", "ATRI", "アイラ", "新堂彩音", 
    "姫野星奏", "小鞠ゆい", "聖代橋氷織", "有坂真白", "白咲美絵瑠", "二階堂真紅"],

    '零之使魔':
    ["ルイズ","ティファニア","イルククゥ","アンリエッタ","タバサ","シエスタ","ハルナ","少女リシュ","リシュ","アキナ","クリス",
    "カトレア","エレオノール","モンモランシー","リーヴル","キュルケ","ウェザリー","サイト","ギーシュ","コルベール","オスマン",
    "デルフリンガー","テクスト","ダンプリメ","ガレット","スカロン"],

    "TOLOVE":
    ["金色の闇","モモ","ナナ","結城美柑","古手川唯","黒咲芽亜","ネメシス","村雨静","セリーヌ","ララ","天条院沙姫",
    "西連寺春菜","ルン","メイ","霧崎恭子","籾岡里紗","沢田未央","ティアーユ","九条凛","藤崎綾","結城華","御門涼子",
    "アゼンダ","夕崎梨子","結城梨斗","ペケ","猿山ケンイチ","レン","校長"],
    
    "赛马娘":
    ["Special Week","Silence Suzuka","Tokai Teio","Maruzensky","Fuji Kiseki","Oguri Cap","Gold Ship","Vodka","Daiwa Scarlet",
    "Taiki Shuttle","Grass Wonder","Hishi Amazon","Mejiro Mcqueen","El Condor Pasa","T.M. Opera O","Narita Brian","Symboli Rudolf",
    "Air Groove","Agnes Digital","Seiun Sky","Tamamo Cross","Fine Motion","Biwa Hayahide","Mayano Topgun","Manhattan Cafe",
    "Mihono Bourbon","Mejiro Ryan","Hishi Akebono","Yukino Bijin","Rice Shower","Ines Fujin","Agnes Tachyon","Admire Vega",
    "Inari One","Winning Ticket","Air Shakur","Eishin Flash","Curren Chan","Kawakami Princess","Gold City","Sakura Bakushin O",
    "Seeking the Pearl","Shinko Windy","Sweep Tosho","Super Creek","Smart Falcon","Zenno Rob Roy","Tosen Jordan","Nakayama Festa",
    "Narita Taishin","Nishino Flower","Haru Urara","Bamboo Memory","Biko Pegasus","Marvelous Sunday","Matikane Fukukitaru","Mr. C.B.",
    "Meisho Doto","Mejiro Dober","Nice Nature","King Halo","Matikane Tannhauser","Ikuno Dictus","Mejiro Palmer","Daitaku Helios","Daitaku Helios",
    "Twin Turbo","Satono Diamond","Kitasan Black","Sakura Chiyono O","Sirius Symboli","Mejiro Ardan","Yaeno Muteki","Tsurumaru Tsuyoshi",
    "Mejiro Bright","Sakura Laurel","Narita Top Road","Yamanin Zephyr","Symboli Kris S","Tanino Gimlet","Daiichi Ruby","Aston Machan","Hayakawa Tazuna",
    "KS Miracle","Kopano Rickey","Hoko Tarumae","Wonder Acute","President Akikawa"]
}

XCW = ['xcw', '小仓唯', '镜华']

genshin = ['派蒙', '凯亚', '安柏', '丽莎', '琴', '香菱', '枫原万叶', '迪卢克', '温迪', '可莉', '早柚', '托马', '芭芭拉',
           '优菈', '云堇', '钟离', '魈', '凝光', '雷电将军', '北斗', '甘雨', '七七', '刻晴', '神里绫华', '雷泽', '神里绫人',
           '罗莎莉亚', '阿贝多', '八重神子', '宵宫', '荒泷一斗', '九条裟罗', '夜兰', '珊瑚宫心海', '五郎', '达达利亚', '莫娜',
           '班尼特', '申鹤', '行秋', '烟绯', '久岐忍', '辛焱', '砂糖', '胡桃', '重云', '菲谢尔', '诺艾尔', '迪奥娜', '鹿野院平藏']

speaker_id = '''
类别:=====柚子=========零之使魔==========TOLOVE==========
id: 0： 绫地宁宁   |0：露易丝          |0：金色暗影
    1： 因幡爱瑠   |1：蒂法妮娅        |1：梦梦
    2： 朝武芳乃   |2：依露库库        |2：娜娜
    3： 常陸茉子   |3：安丽埃塔        |3：結城美柑
    4： 丛雨       |4：塔巴萨          |4：古手川唯
    5： 鞍马小春   |5：谢斯塔          |5：黒咲芽亜
    6： 在原七海   |6：晴奈            |6：涅梅西斯
    7： 四季夏目   |7：少女リシュ      |7：村雨静
    8： 明月栞那   |8：リシュ          |8：雪莉奴      
    9： 墨染希     |9：アキナ          |9：菈菈
    10：火打谷爱衣 |10：克莉丝         |10：天条院沙姫
    11：汐山凉音   |11：卡特莉亚       |11：西連寺春菜
    12：矢来美羽   |12：艾蕾欧诺尔     |12：伦
    13：布良梓     |13：蒙莫朗西       |13：メイ
    14：艾莉娜     |14：リーヴル       |14：霧崎恭子
    15：稲村莉音   |15：丘鲁克         |15：籾岡里紗
    16：尼古拉     |16：ウェザリー     |16：沢田未央
    17：荒神小夜   |17：ウェザリー     |17：提亚悠
    18：大房夕里   |18：サイト         |18：九条凛
    19：淡路萌香   |19：ギーシュ       |19：藤崎綾
    20：安娜       |20：コルベール     |20：結城華
    21：倉端直太   |21：オスマン       |21：御門涼子
    22：枡形兵馬   |22：平贺才人       |22：アゼンダ
    23：扇元樹     |23：テクスト       |23：夕崎梨子
    ====常轨脱离===|24：ダンプリメ     |24：結城梨斗
    0：和泉妃爱    |25：ガレット       |25：沛凯
    1：常磐华乃    |26：スカロン       |26：猿山ケンイチ
    2：锦亚澄      |===美少女万華鏡====|27：连
    3：镰仓诗樱    |0：莲华            |28：校長
    4：龙闲天梨    |1：篝之雾枝        |====缘之空====
    5：和泉里      |2：沢渡雫          |0：春日野穹
    6：新川广梦    |3：亚璃子          |1：天女目瑛 
    7：圣莉莉子    |4：灯露椎          |2：依媛奈绪
                   |5：覡夕莉          |3：渚一叶 
========================galgame==========================        
id: 0： 鹰仓杏璃    《Clover Day's》
    1： 鹰仓杏铃    《Clover Day's》
    2： 艾佩莉娅    《景之海的艾佩莉娅》
    3： 仓科明日香  《苍之彼方的四重奏》
    4： ATRI       《ATRI》 
    5： 艾拉       《可塑性记忆》 
    6： 新堂彩音   《想要传达给你的爱恋》
    7： 姫野星奏   《想要传达给你的爱恋》
    8： 小鞠由依   《想要传达给你的爱恋》
    9： 圣代桥冰织 《糖调！-sugarfull tempering-》
    10：有坂真白   《苍之彼方的四重奏》
    11：白咲美绘瑠 《与你相恋的恋爱Recette》
    12：二阶堂真红 《五彩斑斓的世界》
    =========================赛马娘=========================
    0:特别周       |1：宁静铃鹿        |2：东海帝王
    3:丸善斯基     |4：富士奇石        |5：小栗帽
    6:黄金船       |7：伏特加          |8：大和赤骥
    9:大树快车     |10：草上飞         |11：菱亚马逊
    12:目白麦昆    |13：神鹰           |14：好歌剧
    15:成田白仁    |16：皇帝           |17：气槽
    18:爱丽数码    |19：青云天空       |20：玉藻十字
    21:美妙姿势    |22：琵琶晨光       |23：重炮
    24:曼城茶座    |25：美浦波旁       |26：目白赖恩
    27:菱曙        |28：雪之美人       |29：米浴
    30:艾尼斯风神  |31：爱丽速子       |32：爱慕织姬
    33:稻荷一      |34：胜利奖券       |35：空中神宫
    36:荣进闪耀    |37：真机伶         |38：川上公主
    39:黄金城市    |40：樱花进王       |41：采珠
    42:新光风      |43：东商变革       |44：超级小海湾
    45:醒目飞鹰    |46：荒漠英雄       |47：东瀛佐敦
    48:中山庆典    |49：成田大进       |50：西野花
    51:春丽        |52：青竹回忆       |53：微光飞驹
    54:美丽周日    |55：待兼福来       |56：CB先生
    57:名将户仁    |58：目白多伯       |59：优秀素质
    60:帝皇光辉    |61：诗歌剧         |62：狄杜斯
    63:目白善信    |64：大拓太阳神     |65：双涡轮
    66:里见光钻    |67：北部玄驹       |68：樱花千代
    69:天狼星象征  |70：目白阿尔丹     |71：八重无敌
    72:鹤丸刚志    |73：目白光明       |74：樱花桂冠
    75:成田路      |76：也文摄辉       |77：吉兆
    78:谷野美酒    |79：第一红宝       |80：真弓快车
    81:骏川手纲    |82：凯斯奇迹       |83：小林历奇
    84:北港火山    |85：奇锐骏         |86：PresidentAkikawa
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
    elif choose == "零之使魔":
        speakers, model = speaker_dict["零之使魔"][num], 33
    elif choose == "TOLOVE":
        speakers, model = speaker_dict["TOLOVE"][num], 41
    elif choose == "赛马娘":
        speakers, model = speaker_dict["赛马娘"][num], 61
    else:
        speakers = speaker_dict["柚子"][num]
        if num >= 12:
            model = 31
        elif num >= 7:
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
    category=content[0].split('中配')
    if category[1]!='':
       content=[category[0]+'中配',category[1],content[-1]]
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
    category = content[0].split('日配')
    if category[1]!='':
       content=[category[0]+'日配',category[1],content[-1]]
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
    voice = await A.gethash(text_chjp)
    final_send = MessageSegment.record(voice)
    await bot.send(ev, final_send)

@sv.on_prefix(['#'+i + '日配' for i in XCW])
@sv.on_prefix(['#'+i + '中配' for i in genshin])
@sv.on_prefix(['#'+i + '中配' for i in XCW])
async def voice(bot, ev):
    try:
        text: str = ev.message.extract_plain_text().strip()
        if not text:
            await bot.send(ev, '请输入需要合成语音的文本', at_sender=True)
            return
        preid: str = ev.prefix[1:-2]
        prelang: str = ev.prefix[-2:]
        if prelang == '中配':
            if preid in XCW:
                text = await chinese2katakana(text)
                voice = await voiceApi(XcwAPI + text)
            else:
                text = replace_text(text)
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

   
@sv.on_rex(r'^(语音|配音)(帮助)?$')
async def voicehelp(bot, ev):
    image = Image.open(os.path.join(os.path.dirname(__file__),f"help.jpg"))
    draw= ImageDraw.Draw(image) #建立一个绘图的对象
    font = ImageFont.truetype(os.path.join(os.path.dirname(__file__),f"SIMYOU.ttf"), 35)
    font2 = ImageFont.truetype(os.path.join(os.path.dirname(__file__),f"SIMYOU.ttf"), 30)
    text1=speaker_id                     
    text=''
    textcn=''
    textxcw='[小仓唯/镜华]指令:#小仓唯[中配/日配] + 文本,如#小仓唯日配 你好'
    text2='以下角色无需填写类别,指令#[名字][中配(无日配)] + 文本,如#派蒙中配 你好'
    for prime in genshin:
        text3=text
        text+=prime+" " 
        if len(text)>30:
           if len(text)<33:
              textcn+=text+'\n'
              text=''
           else:
              textcn+=text3+'\n'
              text=''
              text+=prime+" "
    textcn+=text+'\n'    
    draw.text((84,827), text1, font=font, fill="#2e59a7") 
    draw.text((84,2880), textxcw, font=font2, fill="#531dab")
    draw.text((84,2920), text2, font=font2, fill="#531dab")
    draw.text((84,2960), textcn, font=font, fill="#2e59a7") 
    image.save(os.path.join(os.path.dirname(__file__),f"help2.jpg"))
    help2=os.path.join(os.path.dirname(__file__),f"help2.jpg")
    await bot.send(ev, MessageSegment.image(f'file:///{help2}'))


Genshin_list = (
    (',', '，'), ('.', '。'), ('!', '！'), ('?', '？'),(':', '：'),('(', '（'),('<', '《'),('>', '》'), ('0', '零'), ('1', '一'), ('2', '二'), ('3', '三'), ('4', '四'),
    ('5', '五'), ('6', '六'), ('7', '七'), ('8', '八'), ('9', '九'),)

def replace_text(text):
    for en, cn in Genshin_list:
        text = text.replace(en, cn)
    print(text)
    return text
