import numpy as np
from PIL import Image, ImageDraw, ImageFont

def puttext(img, text, position, color, font_size, font_file='yuyang.ttf', align='TL'):
    pilimg = Image.fromarray(img.copy())
    draw_temp = ImageDraw.Draw(pilimg)
    font = ImageFont.truetype(font_file, font_size, encoding="utf-8")
    tw, th = text_size = draw_temp.textsize(text, font)
    x, y = position
    x_start, y_start = x, y
    if 'T' in align:
        y_start = y
    if 'B' in align:
        y_start = y - th
    if 'L' in align:
        x_start = x
    if 'R' in align:
        x_start = x - tw
    if align[0] == 'C':
        y_start = y - th // 2
    if align[1] == 'C':
        x_start = x - tw // 2
    draw_temp.text((x_start, y_start), text, fill=color, font=font)
    img = np.array(pilimg)
    return img.astype(np.uint8)
