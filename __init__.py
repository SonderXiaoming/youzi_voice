from hoshino import Service, priv
from nonebot import MessageSegment
from .create_img import image_draw
from .youdaotranslate import translate
from .getvoiece import voiceApi, GenshinAPI, XcwAPI, Error, chinese2katakana, getvoice
from PIL import Image, ImageDraw, ImageFont
import os

sv_help = """
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
""".strip()

speaker_dict = {
    "柚子": [
        "綾地寧々",
        "因幡めぐる",
        "朝武芳乃",
        "常陸茉子",
        "ムラサメ",
        "鞍馬小春",
        "在原七海",
        "四季ナツメ",
        "明月栞那",
        "墨染希",
        "火打谷愛衣",
        "汐山涼音" "矢来美羽",
        "布良梓",
        "エリナ",
        "稲村莉音",
        "ニコラ",
        "荒神小夜",
        "大房ひよ里",
        "淡路萌香",
        "アンナ",
        "倉端直太",
        "枡形兵馬",
        "扇元樹",
    ],
    "常轨脱离": ["和泉妃愛", "常盤華乃", "錦あすみ", "鎌倉詩桜", "竜閑天梨", "和泉里", "新川広夢", "聖莉々子"],
    "缘之空": ["春日野穹", "天女目瑛", "依媛奈緒", "渚一葉"],
    "美少女万華鏡": ["蓮華", "篝ノ霧枝", "沢渡雫", "亜璃子", "灯露椎", "覡夕莉"],
    "galgame": [
        "鷹倉杏璃",
        "鷹倉杏鈴",
        "アペイリア",
        "倉科明日香",
        "ATRI",
        "アイラ",
        "新堂彩音",
        "姫野星奏",
        "小鞠ゆい",
        "聖代橋氷織",
        "有坂真白",
        "白咲美絵瑠",
        "二階堂真紅",
    ],
    "零之使魔": [
        "ルイズ",
        "ティファニア",
        "イルククゥ",
        "アンリエッタ",
        "タバサ",
        "シエスタ",
        "ハルナ",
        "少女リシュ",
        "リシュ",
        "アキナ",
        "クリス",
        "カトレア",
        "エレオノール",
        "モンモランシー",
        "リーヴル",
        "キュルケ",
        "ウェザリー",
        "サイト",
        "ギーシュ",
        "コルベール",
        "オスマン",
        "デルフリンガー",
        "テクスト",
        "ダンプリメ",
        "ガレット",
        "スカロン",
    ],
    "TOLOVE": [
        "金色の闇",
        "モモ",
        "ナナ",
        "結城美柑",
        "古手川唯",
        "黒咲芽亜",
        "ネメシス",
        "村雨静",
        "セリーヌ",
        "ララ",
        "天条院沙姫",
        "西連寺春菜",
        "ルン",
        "メイ",
        "霧崎恭子",
        "籾岡里紗",
        "沢田未央",
        "ティアーユ",
        "九条凛",
        "藤崎綾",
        "結城華",
        "御門涼子",
        "アゼンダ",
        "夕崎梨子",
        "結城梨斗",
        "ペケ",
        "猿山ケンイチ",
        "レン",
        "校長",
    ],
    "赛马娘": [
        "Special Week",
        "Silence Suzuka",
        "Tokai Teio",
        "Maruzensky",
        "Fuji Kiseki",
        "Oguri Cap",
        "Gold Ship",
        "Vodka",
        "Daiwa Scarlet",
        "Taiki Shuttle",
        "Grass Wonder",
        "Hishi Amazon",
        "Mejiro Mcqueen",
        "El Condor Pasa",
        "T.M. Opera O",
        "Narita Brian",
        "Symboli Rudolf",
        "Air Groove",
        "Agnes Digital",
        "Seiun Sky",
        "Tamamo Cross",
        "Fine Motion",
        "Biwa Hayahide",
        "Mayano Topgun",
        "Manhattan Cafe",
        "Mihono Bourbon",
        "Mejiro Ryan",
        "Hishi Akebono",
        "Yukino Bijin",
        "Rice Shower",
        "Ines Fujin",
        "Agnes Tachyon",
        "Admire Vega",
        "Inari One",
        "Winning Ticket",
        "Air Shakur",
        "Eishin Flash",
        "Curren Chan",
        "Kawakami Princess",
        "Gold City",
        "Sakura Bakushin O",
        "Seeking the Pearl",
        "Shinko Windy",
        "Sweep Tosho",
        "Super Creek",
        "Smart Falcon",
        "Zenno Rob Roy",
        "Tosen Jordan",
        "Nakayama Festa",
        "Narita Taishin",
        "Nishino Flower",
        "Haru Urara",
        "Bamboo Memory",
        "Biko Pegasus",
        "Marvelous Sunday",
        "Matikane Fukukitaru",
        "Mr. C.B.",
        "Meisho Doto",
        "Mejiro Dober",
        "Nice Nature",
        "King Halo",
        "Matikane Tannhauser",
        "Ikuno Dictus",
        "Mejiro Palmer",
        "Daitaku Helios",
        "Daitaku Helios",
        "Twin Turbo",
        "Satono Diamond",
        "Kitasan Black",
        "Sakura Chiyono O",
        "Sirius Symboli",
        "Mejiro Ardan",
        "Yaeno Muteki",
        "Tsurumaru Tsuyoshi",
        "Mejiro Bright",
        "Sakura Laurel",
        "Narita Top Road",
        "Yamanin Zephyr",
        "Symboli Kris S",
        "Tanino Gimlet",
        "Daiichi Ruby",
        "Aston Machan",
        "Hayakawa Tazuna",
        "KS Miracle",
        "Kopano Rickey",
        "Hoko Tarumae",
        "Wonder Acute",
        "President Akikawa",
    ],
    "公主连结": [
        "菈比莉斯塔（Overload）",
        "铃奈（夏日）",
        "杏奈",
        "雪菲",
        "可可萝",
        "菈比莉斯塔",
        "绫音（圣诞节）",
        "碧（插班生）",
        "嘉夜",
        "镜华（万圣节）",
        "珠希",
        "望（夏日）",
        "铃莓",
        "真琴（夏日）",
        "静流（情人节）",
        "咲恋",
        "莉玛",
        "香澄（夏日）",
        "千歌",
        "忍",
        "依里",
        "佩可莉姆（新年）",
        "胡桃",
        "智（魔法少女）",
        "优衣",
        "怜（万圣节）",
        "栞",
        "香织（夏日）",
        "祈梨（时间旅行）",
        "咲恋（夏日）",
        "铃奈",
        "真步（夏日）",
        "亚里莎",
        "镜华",
        "未奏希",
        "伊莉亚（圣诞节）",
        "美里",
        "似似花",
        "克莉丝提娜（圣诞节）",
        "美冬（夏日）",
        "莉玛（灰姑娘）",
        "铃莓（夏日）",
        "古蕾雅",
        "美美（万圣节）",
        "千歌（圣诞节）",
        "碧",
        "雪",
        "惠理子（情人节）",
        "伊绪",
        "拉姆",
        "七七香（夏日）",
        "铃莓（新年）",
        "铃（游骑兵）",
        "环奈",
        "惠理子",
        "可可萝（礼服）",
        "优衣（新年）",
        "望（圣诞节）",
        "可可萝（公主）",
        "纯（夏日）",
        "环奈（振袖）",
        "咲恋（圣诞节）",
        "露娜",
        "香澄（魔法少女）",
        "姬塔",
        "矛依未（新年）",
        "栞（魔法少女）",
        "真步（灰姑娘）",
        "怜（新年）",
        "千歌（夏日）",
        "祈梨",
        "由加莉",
        "佩可莉姆（夏日）",
        "步美（仙境）",
        "可可萝（夏日）",
        "绫音",
        "由加莉（圣诞节）",
        "真阳",
        "雷姆",
        "茜里",
        "铃",
        "凛（偶像大师）",
        "凯露",
        "克罗依（圣学祭）",
        "秋乃",
        "克莉丝提娜",
        "佩可莉姆",
        "露",
        "莫妮卡",
        "璃乃",
        "静流（夏日）",
        "纺希（万圣节）",
        "香澄",
        "美咲",
        "美里（夏日）",
        "智",
        "初音",
        "璃乃（仙境）",
        "卯月（偶像大师）",
        "空花",
        "珠希（夏日）",
        "纯",
        "美美",
        "忍（万圣节）",
        "妮侬（大江户）",
        "千爱瑠",
        "可可萝（新年）",
        "怜（公主）",
        "未奏希、美美、镜华",
        "伊莉亚",
        "望",
        "优衣（公主）",
        "凯露（公主）",
        "克罗依",
        "秋乃（圣诞节）",
        "优衣（礼服）",
        "杏奈（夏日）",
        "静流",
        "未奏希（万圣节）",
        "茜里（天使）",
        "宫子",
        "日和莉（新年）",
        "优妮",
        "安",
        "流夏（夏日）",
        "美冬（工作服）",
        "美冬",
        "初音（夏日）",
        "矛依未",
        "凯露（夏日）",
        "莫妮卡（魔法少女）",
        "香织",
        "宫子（万圣节）",
        "美咲（万圣节）",
        "妮侬",
        "怜",
        "真阳（游骑兵）",
        "碧（工作服）",
        "日和莉",
        "七七香",
        "真琴",
        "步美",
        "深月",
        "日和莉（公主）",
        "伊绪（夏日）",
        "茉莉",
        "佩可莉姆（公主）",
        "空花（大江户）",
        "惠理子（夏日）",
        "凯露（新年）",
        "爱蜜莉雅",
        "依里（天使）",
        "茉莉（万圣节）",
        "真琴（灰姑娘）",
        "纺希",
        "真步",
        "流夏",
        "似似花（新年）",
        "未央（偶像大师）",
        "胡桃（圣诞节）",
        "千爱瑠（圣学祭）",
    ],
    "魔法纪录": [
        "环彩羽(Tamaki Iroha)",
        "环忧(Tamaki Ui)",
        "七海八千代(Nanami Yachiyo)",
        "十咎桃子(Togame Momoko)",
        "水波玲奈(Minami Rena)",
        "秋野枫(Akino Kaede)",
        "八云御魂(Yakumo Mitama)",
        "由比鹤乃(Yui Tsuruno)",
        "深月菲莉希亚(Mitsuki Felicia)",
        "二叶莎奈(Futaba Sana)",
        "梓美冬(Azusa Mifuyu)",
        "佐仓杏子(Sakura Kyōko)",
        "天音月咲(Amane Tsukasa)",
        "天音月夜(Amane Tsukuyo)",
        "里见灯花(Satomi Tōka)",
        "柊音梦(Hiiragi Nemu)",
        "和泉十七夜(Izumi Kanagi)",
        "阿莉娜·格雷(Alina Gray)",
        "蓝家姬奈(Aika Himena)",
        "大庭树里(Ōba：Juri)",
        "宫尾时雨",
        "丘比(QB)",
        "巴麻美(Tomoe Mami)",
    ],
}

XCW = ["xcw", "小仓唯", "镜华"]

genshin = [
    "派蒙",
    "凯亚",
    "安柏",
    "丽莎",
    "琴",
    "香菱",
    "枫原万叶",
    "迪卢克",
    "温迪",
    "可莉",
    "早柚",
    "托马",
    "芭芭拉",
    "优菈",
    "云堇",
    "钟离",
    "魈",
    "凝光",
    "雷电将军",
    "北斗",
    "甘雨",
    "七七",
    "刻晴",
    "神里绫华",
    "雷泽",
    "神里绫人",
    "罗莎莉亚",
    "阿贝多",
    "八重神子",
    "宵宫",
    "荒泷一斗",
    "九条裟罗",
    "夜兰",
    "珊瑚宫心海",
    "五郎",
    "达达利亚",
    "莫娜",
    "班尼特",
    "申鹤",
    "行秋",
    "烟绯",
    "久岐忍",
    "辛焱",
    "砂糖",
    "胡桃",
    "重云",
    "菲谢尔",
    "诺艾尔",
    "迪奥娜",
    "鹿野院平藏",
]

speaker_id = """
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
id: 0:特别周       |1：宁静铃鹿        |2：东海帝王
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
=========================公主连结=========================
id: 1：菈比莉斯塔（Overload） 2：铃奈（夏日）
    3：杏奈                  4：雪菲
    5：可可萝                6：菈比莉斯塔
    7：绫音（圣诞节）         8：碧（插班生）
    9：嘉夜              10：镜华（万圣节）
    11：珠希             12：望（夏日）
    13：铃莓             14：真琴（夏日）
    15：静流（情人节）    16：咲恋
    17：莉玛             18：香澄（夏日）
    19：千歌             20：忍
    21：依里             22：佩可莉姆（新年）
    23：胡桃             24：智（魔法少女）
    25：优衣             26：怜（万圣节）
    27：栞               28：香织（夏日）
    29：祈梨（时间旅行）  30：咲恋（夏日）
    31：铃奈             32：真步（夏日）
    33：亚里莎            34：镜华
    35：未奏希            36：伊莉亚（圣诞节）
    37：美里              38：似似花
    39：克莉丝提娜（圣诞节） 40：美冬（夏日）
    41：莉玛（灰姑娘）     42：铃莓（夏日）
    43：古蕾雅            44：美美（万圣节）
    45：千歌（圣诞节）     46：碧
    47：雪               48：惠理子（情人节）
    49：伊绪             50：拉姆
    51：七七香（夏日）    52：铃莓（新年）
    53：铃（游骑兵）      54：环奈
    55：惠理子           56：可可萝（礼服）
    57：优衣（新年）      58：望（圣诞节）
    59：可可萝（公主）    60：纯（夏日）
    61：环奈（振袖）      62：咲恋（圣诞节）
    63：露娜             64：香澄（魔法少女）
    65：姬塔             66：矛依未（新年）
    67：栞（魔法少女）    68：真步（灰姑娘）
    69：怜（新年）       70：千歌（夏日）
    71：祈梨             72：由加莉
    73：佩可莉姆（夏日）     74：步美（仙境）
    75：可可萝（夏日）       76：绫音
    77：由加莉（圣诞节）     78：真阳
    79：雷姆             80：茜里
    81：铃               82：凛（偶像大师）
    83：凯露             84：克罗依（圣学祭）
    85：秋乃             86：克莉丝提娜
    87：佩可莉姆          88：露
    89：莫妮卡            90：璃乃
    91：静流（夏日）       92：纺希（万圣节）
    93：香澄              94：美咲
    95：美里（夏日）       96：智
    97：初音              98：璃乃（仙境）
    99：卯月（偶像大师）   100：空花
    101：珠希（夏日）      102：纯
    103：美美             104：忍（万圣节）
    105：妮侬（大江户）       106：千爱瑠
    107：可可萝（新年）       108：怜（公主）
    109：未奏希、美美、镜华    110：伊莉亚
    111：望                   112：优衣（公主）
    113：凯露（公主）          114：克罗依
    115：秋乃（圣诞节）        116：优衣（礼服）
    117：杏奈（夏日）          118：静流
    119：未奏希（万圣节）      120：茜里（天使）
    121：宫子               122：日和莉（新年）
    123：优妮               124：安
    125：流夏（夏日）        126：美冬（工作服）
    127：美冬               128：初音（夏日）
    129：矛依未             130：凯露（夏日）
    131：莫妮卡（魔法少女）     132：香织
    133：宫子（万圣节）         134：美咲（万圣节）
    135：妮侬                  136：怜
    137：真阳（游骑兵）         138：碧（工作服）
    139：日和莉                140：七七香
    141：真琴                 142：步美
    143：深月                 144：日和莉（公主）
    145：伊绪（夏日）          146：茉莉
    147：佩可莉姆（公主）      148：空花（大江户）
    149：惠理子（夏日）        150：凯露（新年）
    151：爱蜜莉雅              152：依里（天使）
    153：茉莉（万圣节）        154：真琴（灰姑娘）
    155：纺希                 156：真步
    157：流夏                 158：似似花（新年）
    159：未央（偶像大师）      160：胡桃（圣诞节）
=========================魔法纪录=========================
id: 1：环彩羽(Tamaki Iroha)           2：环忧(Tamaki Ui)
    3：七海八千代(Nanami Yachiyo)     4：十咎桃子(Togame Momoko)
    5：水波玲奈(Minami Rena)          6：秋野枫(Akino Kaede)
    7：八云御魂(Yakumo Mitama)        8：由比鹤乃(Yui Tsuruno)
    9：深月菲莉希亚(Mitsuki Felicia)  10：二叶莎奈(Futaba Sana)
    11：梓美冬(Azusa Mifuyu)          12：佐仓杏子(Sakura Kyōko)
    13：天音月咲(Amane Tsukasa)       14：天音月夜(Amane Tsukuyo)
    15：里见灯花(Satomi Tōka)         16：柊音梦(Hiiragi Nemu)
    17：和泉十七夜(Izumi Kanagi)      18：阿莉娜·格雷(Alina Gray)
    19：蓝家姬奈(Aika Himena)         20：大庭树里(Ōba：Juri)
    21：宫尾时雨                      22：丘比(QB)
""".strip()


def get_speakers(choose, num=0):
    if choose == "常轨脱离":
        speakers, model = speaker_dict["常轨脱离"][num], 5
    elif choose == "缘之空":
        speakers, model = speaker_dict["缘之空"][num], 13
    elif choose == "美少女万華鏡":
        speakers, model = speaker_dict["美少女万華鏡"][num], 17
    elif choose == "galgame":
        speakers, model = speaker_dict["galgame"][num], 29
    elif choose == "零之使魔":
        speakers, model = speaker_dict["零之使魔"][num], 33
    elif choose == "TOLOVE":
        speakers, model = speaker_dict["TOLOVE"][num], 41
    elif choose == "赛马娘":
        speakers, model = speaker_dict["赛马娘"][num], 61
    elif choose == "公主连结":
        speakers, model = speaker_dict["公主连结"][num], 65
    elif choose == "魔法纪录":
        speakers, model = speaker_dict["魔法纪录"][num], 107
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
    name="角色语音模仿",  # 功能名
    use_priv=priv.NORMAL,  # 使用权限
    manage_priv=priv.ADMIN,  # 管理权限
    visible=True,  # False隐藏
    enable_on_default=True,  # 是否默认启用
    help_=sv_help,
)


@sv.on_prefix([i + "中配" for i in speaker_dict.keys()])
async def youzi_voice_cn(bot, ev):
    text = ev.raw_message
    content = text.split()
    category = content[0].split("中配")
    if category[1] != "":
        content = [category[0] + "中配", category[1], content[-1]]
    if len(content) == 2:
        speaker, model = get_speakers(content[0][:-2])
        text_chjp = (
            f"[ZH]{content[1]}[ZH]"
            if content[0][:-2].strip() == "公主连结"
            else await chinese2katakana(content[1])
        )
        A = getvoice(speaker, model)
    elif content[1].isdigit():
        speaker, model = get_speakers(content[0][:-2], int(content[1]))
        text_chjp = (
            f"[ZH]{content[1]}[ZH]"
            if content[0][:-2].strip() == "公主连结"
            else await chinese2katakana(content[1])
        )
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


@sv.on_prefix([i + "日配" for i in speaker_dict.keys()])
async def youzi_voice_ja(bot, ev):
    text = ev.raw_message
    content = text.split()
    category = content[0].split("日配")
    if category[1] != "":
        content = [category[0] + "日配", category[1], content[-1]]
    if len(content) == 2:
        speaker, model = get_speakers(content[0][:-2])
        text_chjp = await translate(content[1])
        if content[0][:-2].strip() == "公主连结":
            text_chjp = f"[JA]{text_chjp}[JA]"
        A = getvoice(speaker, model)
    elif content[1].isdigit():
        speaker, model = get_speakers(content[0][:-2], int(content[1]))
        text_chjp = await translate(content[2])
        if content[0][:-2].strip() == "公主连结":
            text_chjp = f"[JA]{text_chjp}[JA]"
        A = getvoice(speaker, model)
    else:
        await bot.send(ev, sv_help)
        return
    await bot.send(ev, text_chjp)
    voice = await A.gethash(text_chjp)
    final_send = MessageSegment.record(voice)
    await bot.send(ev, final_send)


@sv.on_prefix(["#" + i + "日配" for i in XCW])
@sv.on_prefix(["#" + i + "中配" for i in genshin])
@sv.on_prefix(["#" + i + "中配" for i in XCW])
async def voice(bot, ev):
    try:
        text: str = ev.message.extract_plain_text().strip()
        if not text:
            await bot.send(ev, "请输入需要合成语音的文本", at_sender=True)
            return
        preid: str = ev.prefix[1:-2]
        prelang: str = ev.prefix[-2:]
        if prelang == "中配":
            if preid in XCW:
                text = await chinese2katakana(text)
                voice = await voiceApi(XcwAPI + text)
            else:
                text = replace_text(text)
                voice = await voiceApi(
                    GenshinAPI, {"speaker": preid, "text": text, "length": 1.0}
                )
        else:
            text = await translate(text)
            voice = await voiceApi(XcwAPI + text)
        data = MessageSegment.record(voice)
    except Error as e:
        data = f"发生错误：{e.error}"
        sv.logger.error(data)
    except Exception as e:
        data = f"发生错误：{e}"
        sv.logger.error(data)
    await bot.send(ev, data)


@sv.on_fullmatch("角色id列表")
async def speaker_list(bot, ev):
    img = image_draw(speaker_id)
    await bot.send(ev, f"[CQ:image,file={img}]")


@sv.on_rex(r"^(语音|配音)(帮助)?$")
async def voicehelp(bot, ev):
    image = Image.open(os.path.join(os.path.dirname(__file__), f"help.jpg"))
    draw = ImageDraw.Draw(image)  # 建立一个绘图的对象
    font = ImageFont.truetype(
        os.path.join(os.path.dirname(__file__), f"SIMYOU.ttf"), 35
    )
    font2 = ImageFont.truetype(
        os.path.join(os.path.dirname(__file__), f"SIMYOU.ttf"), 30
    )
    text1 = speaker_id
    text = ""
    textcn = ""
    textxcw = "[小仓唯/镜华]指令:#小仓唯[中配/日配] + 文本,如#小仓唯日配 你好"
    text2 = "以下角色无需填写类别,指令#[名字][中配(无日配)] + 文本,如#派蒙中配 你好"
    for prime in genshin:
        text3 = text
        text += prime + " "
        if len(text) > 30:
            if len(text) < 33:
                textcn += text + "\n"
                text = ""
            else:
                textcn += text3 + "\n"
                text = ""
                text += prime + " "
    textcn += text + "\n"
    draw.text((84, 827), text1, font=font, fill="#2e59a7")
    draw.text((84, 2880), textxcw, font=font2, fill="#531dab")
    draw.text((84, 2920), text2, font=font2, fill="#531dab")
    draw.text((84, 2960), textcn, font=font, fill="#2e59a7")
    image.save(os.path.join(os.path.dirname(__file__), f"help2.jpg"))
    help2 = os.path.join(os.path.dirname(__file__), f"help2.jpg")
    await bot.send(ev, MessageSegment.image(f"file:///{help2}"))


Genshin_list = (
    (",", "，"),
    (".", "。"),
    ("!", "！"),
    ("?", "？"),
    (":", "："),
    ("(", "（"),
    ("<", "《"),
    (">", "》"),
    ("0", "零"),
    ("1", "一"),
    ("2", "二"),
    ("3", "三"),
    ("4", "四"),
    ("5", "五"),
    ("6", "六"),
    ("7", "七"),
    ("8", "八"),
    ("9", "九"),
)


def replace_text(text):
    for en, cn in Genshin_list:
        text = text.replace(en, cn)
    print(text)
    return text
