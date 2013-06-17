#!/opt/local/bin/python3.2
# -*- coding: utf-8 -*-

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
    return args.file_name

def get_names_for_visual(file_name):
    f = open(file_name, "r")
    ngr = ng.Names_calculator(ng.FB2_parser(f.read()).get_text())
    txt_len = ngr.text_len
    f.close()
    names_for_visual = list(ngr.get_names())
    names_for_visual.sort(key = lambda x: x.sort_key(), reverse = True)
    return (names_for_visual[0:hero_count], txt_len)

def main():
    file_name = parse_args()
    (names, txt_len) = get_names_for_visual(file_name)
    image = img.new("RGB", (pic_width, pic_height), "white")
    draw = imgdraw.Draw(image)
    step = int(pic_height/(hero_count + 1))
    text_x  = 24
    x1 = 300
    x2 = 1000
    y = step
    
    font_path = "./TIMCYR.ttf"
    font = ImageFont.truetype(font_path, 16)

    for i in range(hero_count):
        draw.text([text_x, y], names[i].name, fill = 'black', font=font)
        draw.line([x1, y, x2, y], fill = 'black')
        for pos in names[i].positions:
            line_pos = int(pos/txt_len * (x2-x1)) + x1
            up_corner = [line_pos, y + 4]
            down_corner = [line_pos, y - 4]
            left_corner = [line_pos - 4, y]
            right_corner = [line_pos + 4, y]
            corners = up_corner + right_corner + down_corner + left_corner
            draw.polygon(corners, fill = 'orange')
        y += step 

    image.save("pics/" + file_name.split('/')[-1].split('.')[0] + '.png', "PNG")

if __name__ == "__main__":
    main()
