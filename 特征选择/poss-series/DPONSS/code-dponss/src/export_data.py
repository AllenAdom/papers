import sys
import re
import os
import csv
HOME_PATH = '/data/experiments'
RECORD_PATH = '{}/records'.format(HOME_PATH)
RESULT_PATH = '{}/result'.format(HOME_PATH)

def extract_data_from_file(file_name):
   ff_handle = open(file_name, 'r')
   collection = [f for f in ff_handle.readlines()]
   #correlation = l1.split(':')[1]
   inacc_correlation = re.findall(r'\d+\.?\d*', collection[-7])[0]
   correlation = re.findall(r'\d+\.?\d*', collection[-6])[0]
   reducertime = re.findall(r'\d+\.?\d*', collection[-1])[0]
   stage1time = re.findall(r'\d+\.?\d*', collection[-4].split(':')[1])[0]
   stage2time = re.findall(r'\d+\.?\d*', collection[-3].split(':')[1])[0]
   return inacc_correlation, correlation, stage1time, stage2time, reducertime

def export_data(dataname):
   folder_path = '{}/{}'.format(RECORD_PATH, dataname)
   existedDataFileDict = {}
   result_dict = {}
   for relativeFileName in os.listdir(folder_path):
     record_file_name = '{}/{}'.format(folder_path, relativeFileName)
     #extract info
     record_itm = relativeFileName.split('.')[0].split('_')
     data_name = record_itm[0]
     assert data_name == dataname
     algorithm = record_itm[1]
     the_m = int(re.search('\d+', record_itm[2]).group())
     the_k = int(re.search('\d+', record_itm[3]).group())
     the_t = int(re.search('\d+', record_itm[4]).group())

     if not result_dict.has_key(algorithm):
       result_dict[algorithm] = {}
     if not result_dict[algorithm].has_key(the_m):
       result_dict[algorithm][the_m] = {}
     inacc_correlation, correlation, stage1time, stage2time, reducertime = extract_data_from_file(record_file_name)
     result_dict[algorithm][the_m][the_t] = (inacc_correlation, correlation, stage1time, stage2time, reducertime)
   # record to file
   for alg_name, al_item in result_dict.items():
        result_data = open('{}/full_{}_{}.csv'.format(RESULT_PATH, dataname, alg_name), 'w')
        csv_r = csv.writer(result_data)
        csv_r.writerow(['m', 't', 'inaccurate correlation', 'accurate correlation', 'max reducer time', 'stage1', 'stage2', 'total'])
        for m, t_item in al_item.items():
          for t, content in t_item.items():
             csv_r.writerow([m, t, content[0], content[1], content[4], content[2], content[3], str(float(content[3]) + float(content[4]))])
        result_data.close()

if __name__ == "__main__":
  for iname in sys.argv[1:]:
     export_data(iname)
