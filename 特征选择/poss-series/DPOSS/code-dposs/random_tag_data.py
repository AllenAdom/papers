import numpy as np
import sys
# usage: python random_tag_data.py 10 1
num = int(sys.argv[1])
seq = int(sys.argv[2])

ff = open('gisette_normalized.txt','r')
ff_ = open('gisette_tag%d_%d.txt' % (num, seq), 'w')

total = 0
collection = []

# read lines
for line in ff:
  collection.append(line)
  total += 1

# how many rows for each slice
split_ = int(total/num)
print total
print num
print split_

# shuffle the data for generating data slices
seq_list = total * [1]
for i in range(num):
  seq_list[split_*i : (i + 1)*split_] = split_*[i+1]
np.random.shuffle(seq_list)

# To each row, add its sequential number of data slices at the beginning of data
for i in range(total):
  seq = seq_list[i]
  ff1 = str(seq) + ' ' + collection[i]
  ff_.write(ff1)
ff.close()
ff_.close()
