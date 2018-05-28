import re
import sys
import glob
import math
import string
import numpy as np

dictionary = []
total = 300
dt_list = {}

def cosine(a,b):
	result = 0
	length1 = 0
	length2 = 0
	for (i, j) in zip(a, b):
		result += i * j
		length1 += i**2
		length2 += j**2
	return result / math.sqrt(length1 * length2)

def euclid(a,b):
	result = 0
	for (i, j) in zip(a, b):
		result += (i - j) ** 2
	return result

def build_dictionary():
	global dictionary
	global dt_list
	for file in glob.glob('./base/*'):
		with open(file, 'r') as f:
			words = re.sub(r'[{}0-9\n]+'.format(string.punctuation),' ',f.read()).lower()
			# with open(file.replace('base', 'clean'), 'w') as g:
			# 	g.write(words)
			for item in list(set(words.split(' '))):
				if len(item) > 1:
					if item not in dictionary:
						dictionary.append(item)
						dt_list[item] = 1
					else:
						dt_list[item] += 1
	dictionary = sorted(dictionary)

def solve():
	global dictionary
	global dt_list
	# common_matrix = [[0] * len(dictionary)] * len(dictionary)  
	common_matrix = np.zeros((len(dictionary), len(dictionary)))
	for i in range(total):
		vector = [0] * len(dictionary)
		with open('./clean/{}'.format(i), 'r') as f:
			for item in f.read().split(' '):
				if len(item) > 1:
					vector[dictionary.index(item)] += 1
		for j in range(len(vector)):
			if vector[j] != 0:
				for k in range(j + 1, len(vector)):
					if vector[k] != 0:
						common_matrix[j][k] += 1

		length = 0
		for j in range(len(vector)):
			vector[j] = vector[j] * (math.log((1 + total) / (1 + dt_list[dictionary[j]])) + 1)
			length += vector[j] ** 2
		
		for j in range(len(vector)):
			vector[j] /= math.sqrt(length)
		# with open('./tfidf/{}'.format(i), 'w') as g:
		# 	for j in range(len(dictionary)):
		# 		g.write('({},{})  {}\n'.format(i,j,vector[j]))
	for p in range(len(dictionary)):
		for q in range(p):
			common_matrix[p][q] = common_matrix[q][p]
	document = 8
	top_e = [(0,sys.maxsize)] * 5
	top_c = [(0,0)] * 5
	x = []
	y = []
	with open('./tfidf/8', 'r') as f:
		for line in f.readlines():
			try:
				x.append(float(line.split(' ')[-1]))
			except:
				break

	assert(len(x) == len(dictionary))
	for k in range(total):
		if k != document:
			with open('./tfidf/{}'.format(k), 'r') as g:
				for line in g.readlines():
					try:
						y.append(float(line.split(' ')[-1]))
					except:
						break
			e = euclid(x, y)
			c = cosine(x ,y)
			if e < top_e[-1][1]:
				top_e[-1] = (k,e)
			if c > top_c[0][1]:
				top_c[0] = (k,c)
			y = []
			top_e = sorted(top_e, key=lambda d : d[1])
			top_c = sorted(top_c, key=lambda d : d[1])
	print(top_e)
	print(top_c)

	words = 12
	top_e = [(0, sys.maxsize)] * 5
	top_c = [(0, 0)] * 5
	for k in range(len(dictionary)):
		if k != words:
			e = euclid(common_matrix[words], common_matrix[k])
			c = cosine(common_matrix[words], common_matrix[k])
			if e < top_e[-1][1]:
				top_e[-1] = (k,e)
			if c > top_c[0][1]:
				top_c[0] = (k,c)
			top_e = sorted(top_e, key=lambda d : d[1])
			top_c = sorted(top_c, key=lambda d : d[1])

	print()

	print(dictionary[words])
	for item in top_e:
		print(dictionary[item[0]])
	for item in top_c:
		print(dictionary[item[0]])

	# with open('./matrix', 'w') as h:
	# 	for p in range(len(dictionary)):
	# 		for q in range(len(dictionary)):
	# 			h.write(str(common_matrix[p][q]) + ' ')
	# 		h.write('\n')


build_dictionary()
solve()