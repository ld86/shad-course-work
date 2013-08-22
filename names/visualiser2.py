#!/usr/bin/python3.2
#_*_ coding: utf-8 _*_

import PIL.Image as img
import PIL.ImageDraw as imgdraw
import PIL.ImageFilter as imgfilter
import names_grep as ng
import PIL.ImageFont as ImageFont
import argparse

pic_height = 4096
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
    names_for_visual = ngr.get_names()
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
    font_path = "./DejaVuSerif.ttf"
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
        
        height_lst = []
        for j in counts:
            height_lst.append(height * j / max_cnt)

        height_lst[1] = (height_lst[1] + height_lst[2] + height_lst[0]) / 3
        height_lst[-2] = (height_lst[-2] + height_lst[-3] + height_lst[-1]) / 3
        for j in range(2, x2 - x1 - 2):
            local_sum = 0
            for k in range(j - 2, j + 3):
                local_sum += height_lst[k]
            height_lst[j] = local_sum/5

        for j in range(x2 - x1):
            x_coord = j + x1
            red = 255 - int(height_lst[j] * 255 / height)
            green = ', 100, '
            blue = int(height_lst[j] * 255 / height)
            local_color = 'rgb(' + str(red) + green + str(blue) + ')'
            draw.line([x_coord, y, x_coord, y - height_lst[j]], fill = local_color)
        y += step 

    image.save("pics/" + file_name.split('/')[-1].split('.')[0] + '.v4.png', "PNG")

def main():
    run(parse_args())

if __name__ == "__main__":
    main()
