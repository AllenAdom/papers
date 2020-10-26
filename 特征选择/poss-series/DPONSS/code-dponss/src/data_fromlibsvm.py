import numpy as np
import pdb

# ff is the original data file
# ff_ is the transposed data
# ffxx is the labels which is also transposed
ff = open('gisette_scale_raw.txt','r')
ff_ = open('gisette_data.txt', 'wb')
ffxx = open('gisette_labels.txt', 'wb')

total = 0
count = 0
seq = 0
collection = []
largest_column_num = 0
column_num_remain = 0

# find the largest column number
for line in ff:
  total += 1
  l_ = line.split() # split based on space/tab/enter
  collection.append(l_)
  last_column_num = int(l_[-1].split(':')[0])
  if last_column_num > largest_column_num:
    largest_column_num = last_column_num

column_num_remain = largest_column_num

# fill zeor
data_arr = np.zeros((total, largest_column_num + 1), dtype=np.float16) # last column contains labels!
for i in range(total):
   raw_line = collection[i]
   data_arr[i, -1] = float(raw_line[0])
   for c_item in raw_line[1:]:
     item_list = c_item.split(':')
     indx_ = int(item_list[0])
     value_ = float(item_list[1])
     data_arr[i, indx_ - 1] = value_

# delete columns with zero std values
column_indx_delete = []
for i in range(largest_column_num):
   if data_arr[:, i].std == 0:
     column_indx_delete.append(i)

data_arr = np.delete(data_arr, column_indx_delete, axis=1)
print '%s columns are deleted' % (len(column_indx_delete))

# transpose
tmp_m2 = data_arr.transpose()


print '%s lines in total' % total
print '%s columns' % (largest_column_num - len(column_indx_delete))

# writes transposed data into file
for i in range(largest_column_num):
  num_list = tmp_m2[i, :].tolist()
  l_ = " ".join([str(x) for x in num_list])
  ff_.write(l_+'\n')
# write labels into file
ffxx.write(" ".join([ str(x) for x in tmp_m2[-1,:].tolist()]))
ff.close()
ff_.close()
ffxx.close()
