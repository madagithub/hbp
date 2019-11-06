import json
import csv

with open('translate-pl.csv', 'r') as csvFile:
	reader = csv.reader(csvFile, delimiter=',')
	isFirst = True
	texts = {}
	headerRow = None
	for row in reader:
		if isFirst:
			isFirst = False
			headerRow = row
			for i in range(1, len(row)):
				texts[row[i]] = {}
		else:
			for i in range(1, len(row)):
				texts[headerRow[i]][row[0]] = row[i]

	with open('config.json', 'r') as jsonFile:
		data = json.load(jsonFile)

	for lang in list(data['texts'].keys()):
		if lang != 'en':
			print('Deleting', lang)
			del data['texts'][lang]

	for lang in texts.keys():
		if lang != 'en':
			print('Adding', lang)
			data['texts'][lang] = texts[lang]

	with open('config-output.json', 'w') as jsonFile:
		json.dump(data, jsonFile, ensure_ascii=False, indent='\t')



