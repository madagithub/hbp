import json
import csv
import sys

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('Usage: python3 extract-translation-csv.py lang1.json lang2.json ...')
    else:
        fileToKeyToValue = {}

        for i in range(1, len(sys.argv)):
            fileName = sys.argv[i]
            with open(fileName, 'r') as file:
                fileToKeyToValue[fileName] = {}
                items = json.load(file)['items']
                for item in items:
                    fileToKeyToValue[fileName][item['key']] = item['value']

        header = ['Key'] + list(fileToKeyToValue.keys())
        rows = [header]

        for key in list(fileToKeyToValue[sys.argv[1]].keys()):
            row = []
            row.append(key)
            for file in fileToKeyToValue.keys():
                row.append(fileToKeyToValue[file][key])

            rows.append(row)

        with open('translate.csv', 'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(rows)
