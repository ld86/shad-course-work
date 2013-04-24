import sys
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFilter as ImageFilter
import math

def save_dialog_picture(book, save_path):
    HEIGHT = 160
    WIDTH = 1024

    metrics = book.metrics()
    sentences_count = metrics.get_sentences_count()
    positions = metrics.get_dialogs_positions()

    image = Image.new("RGBA", (WIDTH, HEIGHT), (0,0,0,0))
    draw = ImageDraw.Draw(image)

    counts = [0 for i in range(WIDTH)]
	
    for position in positions[:-1]:
        x = int((float(position)/sentences_count) * WIDTH)
        counts[x] += 1
		
    new_counts = []
    for i in range(0,len(counts)-0):
        new_counts.append(float(sum(counts[i-4:i+4]))/9)
		
    counts = new_counts
		
    max_count = max(counts)
    pow = 1.3
    max_count_exp = math.pow(pow, max(counts))
	
    for i in zip(counts, range(len(counts))):
        color = int(255 - (float(i[0])/max_count) * 255)
        height = int(HEIGHT - (float(i[0])/max_count) * HEIGHT)
        draw.line([(i[1], HEIGHT), (i[1], height)], fill=(color,color,128))	

    image.save("%s" % save_path, "PNG")
