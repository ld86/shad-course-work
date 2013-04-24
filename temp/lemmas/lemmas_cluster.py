#!/usr/bin/python

from hcluster import pdist, linkage, dendrogram
from matplotlib.pylab import show, savefig, gcf
from random import choice
import math

def get_metric(first_set, second_set):
	min_length = min(len(first_set), len(second_set))	
	intersection = first_set.intersection(second_set)
	rank = float(len(intersection)) / float(min_length)
	return 1 / rank

raw_metrics = open('result').read().split('\n')[:-1]
parsed = []

for line in raw_metrics:
	splitted = line.split(';')
	splitted[2] = set(splitted[2].split(','))
	parsed.append(splitted)

indexes = list(range(len(raw_metrics)))
choosen = [ (choice(indexes),) for i in range(400)]

choosen = list(set(choosen))

metric = lambda a, b: get_metric(parsed[int(a[0])][2], parsed[int(b[0])][2])
label = lambda a: parsed[choosen[a][0]][1]


dendrogram(linkage(pdist(choosen, metric), 'complete'), leaf_label_func=label, color_threshold=6)
fig = gcf()
fig.set_size_inches(20,12)
savefig('image.png', dpi=400, bbox_inches='tight')
