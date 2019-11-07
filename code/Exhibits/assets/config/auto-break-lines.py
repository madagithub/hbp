import json
import csv

MAX_CHARS = 70

def auto_break_lines(text):
	single_line = text.replace('\n', ' ')
	lines = []
	words = single_line.split(' ')
	curr_line = []
	curr_line_length = 0
	for word in words:
		if curr_line_length + len(word) > MAX_CHARS:
			lines.append(curr_line)
			curr_line = []
			curr_line_length = 0

		curr_line.append(word)
		curr_line_length += len(word) + 1

	if curr_line_length > 0:
		lines.append(curr_line)

	result = ''
	for line in lines:
		line_text = ' '.join(line)
		result += line_text + '\n'
	
	return result

with open('config.json', 'r') as jsonFile:
	data = json.load(jsonFile)

	for lang in list(data['texts'].keys()):
		if lang != 'en':
			for key in list(data['texts'][lang].keys()):
				if '_DESC' in key and 'OS_MAP_' in key:
					text = data['texts'][lang][key]
					data['texts'][lang][key] = auto_break_lines(text)

	with open('config-output.json', 'w') as jsonFile:
		json.dump(data, jsonFile, ensure_ascii=False, indent='\t')
