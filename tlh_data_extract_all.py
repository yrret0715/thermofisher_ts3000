import sys, os


for root, dir, files in os.walk('/Users/tien-linhsieh/workspace/tlh_ChemE_data/process'):
	print(files)

	for file in files:
		print(file)
		if file.endswith('.xls'):
			os.system('python tlh_data_extract2.py {}'.format(file))

			

