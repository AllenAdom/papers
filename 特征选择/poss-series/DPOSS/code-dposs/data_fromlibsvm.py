import numpy as np
import pdb

ff = open('gisette_scale.t','r')
ff_ = open('gisette_normalized.txt', 'w')
ffxx = open('gisette_normalized_label.txt', 'w')


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
data_arr = np.zeros((total, largest_column_num + 1)) # last column is labels!
for i in range(total):
   raw_line = collection[i]
   data_arr[i, -1] = float(raw_line[0])
   for c_item in raw_line[1:]:
     item_list = c_item.split(':')
     indx_ = int(item_list[0])
     value_ = float(item_list[1])
     data_arr[i, indx_ - 1] = value_

# normalization
# delete columns with all zero and std is zeor
column_indx_delete = []
for i in range(largest_column_num):
  non_zeros_indx = data_arr[:, i].nonzero()
  # prepare to delete the column full of zeros
  if non_zeros_indx[0].size == 0:
    column_indx_delete.append(i)
    column_num_remain  -= 1
    continue
  column_mean = np.mean(data_arr[:, i])
  column_std = np.std(data_arr[:, i])

  # prepare to delete the column with zero std
  if column_std  == 0.:
    column_indx_delete.append(i)
    column_num_remain  -= 1
    continue
  data_arr[:, i] = (data_arr[:, i] - column_mean)/column_std

# for labels
label_column_mean = np.mean(data_arr[:, -1])
label_column_std = np.std(data_arr[:, -1])
data_arr[:, -1] = (data_arr[:, -1] - label_column_mean)/label_column_std
  
# delete columns
data_arr=np.delete(data_arr, column_indx_delete, axis=1)

tmp_m2 = data_arr.transpose()

print '%s total' % total
print '%s columns => %s columns (%s)' % (largest_column_num, column_num_remain, tmp_m2.shape[0])

# writes transposed data into file
for i in range(column_num_remain):
  num_list = tmp_m2[i, :].tolist()
  l_ = " ".join([str(x) for x in num_list])
  ff_.write(l_+'\n')
# write labels into file
ffxx.write(" ".join([ str(x) for x in tmp_m2[-1,:].tolist()]))
ff.close()
ff_.close()
ffxx.close()
