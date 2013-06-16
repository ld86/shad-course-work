#!/usr/bin/python3.2
#_*_ coding: utf-8 _*_

import PIL.Image as img
import PIL.ImageDraw as imgdraw
import PIL.ImageFilter as imgfilter
import names_grep as ng
import PIL.ImageFont as ImageFont
import argparse

pic_height = 1024
pic_width = 1024
hero_count = 20

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", type = str)
    args = parser.parse_args()
    print(args.file_name)
    return args.file_name

def get_names_for_visual(file_name):
    f = open(file_name, "rb")
    file_text = f.read()
    pure_text = ng.FB2_parser(file_text).get_text()
    ngr = ng.Names_calculator(pure_text)
    txt_len = ngr.text_len
    f.close()
    names_for_visual = list(ngr.get_names())
    names_for_visual.sort(key = lambda x: x.sort_key(), reverse = True)
    return (names_for_visual[0:hero_count], txt_len)

def run(file_name):
    (names, txt_len) = get_names_for_visual(file_name)
    image = img.new("RGB", (pic_width, pic_height), "white")
    draw = imgdraw.Draw(image)
    step = int(pic_height/(hero_count + 1))
    text_x  = 24
    x1 = 300
    x2 = 1000
    y = step 
    font_path = "/usr/share/fonts/truetype/ttf-dejavu/DejaVuSerif.ttf"
    font = ImageFont.truetype(font_path, 16)
    height = step
    max_cnt = 0
    for i in range(hero_count):
        counts = [0 for i in range(x2 -  x1)]
        for pos in names[i].positions:
            x = int((pos / txt_len) * (x2 - x1))
            counts[x] += 1
        mc = max(counts)
        if max_cnt < mc:
            max_cnt = mc
    for i in range(hero_count):
        draw.text([text_x, y], names[i].name, fill = 'black', font=font)
        draw.line([x1, y, x2, y], fill = 'black')
        counts = [0 for i in range(x2 -  x1)]
        for pos in names[i].positions:
            x = int((pos / txt_len) * (x2 - x1))
            counts[x] += 1
        for i in zip(counts, range(x2 - x1)):
            x_coord = i[1] + x1
            draw.line([x_coord, y, x_coord, y - height * i[0] / max_cnt], fill = 'blue')
        y += step 

    image.save("pics/" + file_name.split('/')[-1].split('.')[0] + '2.png', "PNG")

def main():
    run(parse_args())

if __name__ == "__main__":
    main()
