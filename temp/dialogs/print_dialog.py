#!/usr/bin/python3

import sys
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFilter as ImageFilter

HEIGHT = 160
WIDTH = 1024

def main(argv):
    filename = argv[1]
    raw = []
    with open(filename) as f:
        raw = f.read().split('\n')
    positions = raw[1:]
    sentences_count = float(raw[0])

    image = Image.new("RGBA", (WIDTH, HEIGHT), (0,0,0,0))
    draw = ImageDraw.Draw(image)

    counts = [0 for i in range(WIDTH)]

    for position in positions[:-1]:
        x = int((float(position)/sentences_count) * WIDTH)
        counts[x] += 1        

    for i in zip(counts, range(len(counts))):
        draw.line([(i[1], HEIGHT), (i[1], HEIGHT - 10 * i[0])], fill="black")
    
    image.filter(ImageFilter.BLUR).save("%s.png" % filename, "PNG")

if __name__ == "__main__":
    main(sys.argv)
