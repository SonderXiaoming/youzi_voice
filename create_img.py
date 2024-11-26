import io
import base64
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

LINE_CHAR_COUNT = 40 * 2  # 每行字符数：30个中文字符(=60英文字符)
LINE_CHAR_COUNT_MAX = 0
CHAR_SIZE = 32
CHAR_SIZE_h = 47
TABLE_WIDTH = 4

frame_path = Path(__file__).parent


def line_break(line):
    global LINE_CHAR_COUNT_MAX
    LINE_CHAR_COUNT_MAX = 0
    ret = ""
    width = 0
    for c in line:
        if len(c.encode("utf8")) == 3:  # 中文
            if LINE_CHAR_COUNT == width + 1:  # 剩余位置不够一个汉字
                width = 2
                ret += "\n" + c
            else:  # 中文宽度加2，注意换行边界
                width += 2
                ret += c
        else:
            if c == "\t":
                space_c = TABLE_WIDTH - width % TABLE_WIDTH  # 已有长度对TABLE_WIDTH取余
                ret += " " * space_c
                width += space_c
            elif c == "\n":
                width = 0
                ret += c
            else:
                width += 1
                ret += c
        if width >= LINE_CHAR_COUNT:
            ret += "\n"
            width = 0
            LINE_CHAR_COUNT_MAX = LINE_CHAR_COUNT
        if width > LINE_CHAR_COUNT_MAX:
            LINE_CHAR_COUNT_MAX = width

    if ret.endswith("\n"):
        return ret
    return ret + "\n"


def image_draw(msg):
    global LINE_CHAR_COUNT_MAX
    output_str = line_break(msg)
    fontpath = os.path.dirname(os.path.realpath(__file__)) + "/SIMYOU.ttf"
    d_font = ImageFont.truetype(fontpath, CHAR_SIZE)
    lines = output_str.count("\n")  # 计算行数

    image = Image.new(
        mode="RGB",
        size=(LINE_CHAR_COUNT_MAX * CHAR_SIZE // 2 + 84, CHAR_SIZE_h * lines + 84),
        color=(255, 252, 245),
    )
    draw_table = ImageDraw.Draw(im=image)
    draw_table.text(
        xy=(42, 42),
        text=output_str,
        fill=(125, 101, 89),
        font=d_font,
        spacing=CHAR_SIZE // 2,
    )  # spacing调节机制不清楚如何计算
    draw_table.rectangle(
        xy=(
            16,
            16,
            LINE_CHAR_COUNT_MAX * CHAR_SIZE // 2 + 69,
            CHAR_SIZE_h * lines + 69,
        ),
        fill=None,
        outline=(220, 211, 196),
        width=2,
    )
    b_io = io.BytesIO()
    image.save(b_io, format="JPEG")
    base64_str = "base64://" + base64.b64encode(b_io.getvalue()).decode()
    return base64_str
