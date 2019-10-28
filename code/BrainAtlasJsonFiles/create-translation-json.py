import json
import csv
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 extract-translation-csv.py texts.csv')
    else:
        csvFilename = sys.argv[1]
        fileToItems = {}
        with open(csvFilename, newline='') as csvFile:
            reader = csv.reader(csvFile, delimiter=',')
            isHeader = True
            header = []
            for row in reader:
                if isHeader:
                    header = row
                    for i in range(1, len(row)):
                        fileToItems[row[i]] = []
                    isHeader = False
                else:
                    for i in range(1, len(row)):
                        fileToItems[header[i]].append({'key': row[0], 'value': row[i]})

        for fileName in list(fileToItems.keys()):
            with open(fileName + '.new', 'w') as jsonFile:
                json.dump({'items': fileToItems[fileName]}, jsonFile, ensure_ascii=False, indent='\t')

