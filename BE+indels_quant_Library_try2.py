import csv
import pandas as pd
import os
import glob
import re
import sys

os.chdir("/Users/mneugeba/Dropbox/LiuLab/Miseq/" + str(sys.argv[1]))
#so argv[1] is folder name, argv[2] is the base I want, and argv [3] is what I want it changed to. Maybe I can change it to C T 6 (where 6 is the target)
#this version is agnostic to sites used

"""
amplicons = ['H2', 'H3', 'H4', 'R2', 'E1', 'FF', 'NMG657', 'NMG662', 'NMG664', 'NMG708', 'FF1', 'SaH3', '62a', '67b26', '67b34', '67b38', '67b39', '67b41', 'B1', 'NewNG1', 'NewNG2', 'NewNG3', 'NewNG4', 'NewNG5', 'NewNG6']

amplicon_targetC = {'H2': [4,6], 'H3': [4,5,9], 'H4': [3,5,8], 'R2': [3,6,12], 'E1': [5,6], 'FF': [6,7,8,11], 
'NMG657': [9,12,19], 'NMG662': [6,9,10,14,15], 'NMG664': [5,16], 'NMG708': [15], 'FF1': [7,8,12], 'SaH3': [2,8,10,11], 
'62a': [5,8], '67b26': [3,7,8,14], '67b34': [6,7,8], '67b38': [5,12,14], '67b39': [5,9], '67b41': [4,6,12],
'B1': [5,6,7,8,9,10,11,13],
'NewNG1': [5,7], 'NewNG2': [7,9], 'NewNG3': [6,7,8], 'NewNG4': [6,7], 'NewNG5': [4,5], 'NewNG6': [5,6,7]}
"""
desired_editors = ''

# '^((?!dSa).)*$'

#special dictionary that's ideal for nested dicts
class Vividict(dict):
	def __missing__(self, key):
		value = self[key] = type(self)() # retain local pointer to value
		return value                     # faster to return than dict lookup

output_dfs = []

amplicons = [amplicon[:-1] for amplicon in sorted(glob.glob('*/'))]

for amplicon_name in amplicons:
	#create data dictionary 'editor' : {base_index : {'nucleotide' : percentage}}
	with open(glob.glob(amplicon_name + '/*summary.txt')[0], newline='') as f:
		reader = csv.reader(f, delimiter='\t')
		row1 = next(reader)
		amplicon = row1[2:]
		data = Vividict()
		for row in reader:
			for base_index in range(len(amplicon)):
				data[row[0].split('_')[0]][base_index][row[1]] = 100*float(row[base_index + 2])

	#find sgRNA for amplicon
	database = pd.read_csv('/Users/mneugeba/Dropbox/LiuLab/Miseq/AmpliconList2.csv', index_col='name_prefix')

	#get guide sequence for desired amplicon	
	sgRNA = database['g'][amplicon_name]

	amplicon_str = ''.join(amplicon)
	sgRNA_start = amplicon_str.find(sgRNA)

	#get positions of all target bases in protospacer
	#amplicon_target = [m.start() + 1 for m in re.finditer(str(sys.argv[2]), sgRNA)]
	amplicon_target = [int(sys.argv[4])]
	#amplicon_code = 
	context = sgRNA[(int(sys.argv[4])-2):(int(sys.argv[4])+1)]
	target = sgRNA[(int(sys.argv[4]))-1]
	print (amplicon_target, sgRNA, context)
	#amplicon_target = [sys.argv[4]]#trying out the specification of position 6
	#tabulate output data (desired CtoT)
	#make dict with editor
	output_data = {key : [] for key in data.keys()}
	columns = [str(sys.argv[2]) + str(x) for x in amplicon_target]
	for index in amplicon_target:
		for editor in data.keys():
			output_data[editor].append(data[editor][sgRNA_start + index - 1][str(sys.argv[3])])
	output_df = pd.DataFrame.from_dict(output_data, orient='index', columns=columns)
	if desired_editors:
		output_df = output_df.filter(regex=desired_editors, axis=0)
	output_df.sort_index(inplace=True)
	#get indel data
	indels = pd.read_csv(glob.glob(amplicon_name + '/*_quantification_of_editing_frequency.txt')[0], delimiter='\t')
	indels['indel percentage'] = (indels['Only Insertions'] + indels['Only Deletions'] + indels['Insertions and Deletions'] + indels['Insertions and Substitutions'] + indels['Deletions and Substitutions'] + indels['Insertions Deletions and Substitutions'])/indels['Reads_aligned']*100
	indels['Batch'] = indels['Batch'].apply(lambda x: x.split('_')[0])
	indels.set_index('Batch', inplace=True)
	indels.sort_index(inplace=True)
	output_df['Target'] = target#.astype(string)
	output_df['Context'] = context#.astype(string)
	output_df['Indels'] = indels['indel percentage'].astype(float)
	output_df['Total input reads'] = indels['Reads_in_input'].astype(int)
	output_df['Aligned reads'] = indels['Reads_aligned'].astype(int)
	output_df['Fraction aligned reads'] = output_df['Aligned reads']/output_df['Total input reads']

	output_dfs.append(output_df)
	appended_data = pd.DataFrame()
writer = pd.ExcelWriter('BE_quant_' + sys.argv[2] + 'to' + sys.argv[3] + '_pos'+ str(sys.argv[4])+'.xlsx')
row = 0
#rows = output_df.values.tolist()

for index in range(len(output_dfs)):
		#append_df_to_excel(writer,output_dfs[index])
		output_dfs[index].to_excel(writer, startrow=row, header=0)
		row = row + 1
		
#for row in rows:
#	writer.append(row)

writer.save()
writer.close()
#writer.save()
#output_dfs.to_excel(writer)

#writer = pd.ExcelWriter('BE_quant_' + sys.argv[2] + 'to' + sys.argv[3] + 'pos'+ sys.argv[4].xlsx')))))))))))
#with pd.ExcelWriter('BE_quant_' + sys.argv[2] + 'to' + sys.argv[3] + '.xlsx') as writer:
	#output_dfs.to_excel(writer, str(amplicons[index]))
#	for index in range(len(output_dfs)):
#		append_dfs[index].to_excel(writer, str(amplicons[index]))
		#output_dfs[index].to_excel(writer, str(amplicons[index]))
		#
		#
		#
		#
		#
		#
