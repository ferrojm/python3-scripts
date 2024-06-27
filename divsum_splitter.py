#!/usr/bin/env python3

#DIVSUM_SPLITER. searches for the 'Div' string in a divsum file and exports a new table (file.csv)
#usage divsum_spliter file

import sys
import csv

def divsum_splitter(file):
    file_modif = file.split('.')[0]
    with open(file) as file, open( file_modif + '.csv', 'w') as modif:
        orig_table = csv.reader(file)
        for row in orig_table:
            for index in row:
                if 'Div' in index:
                    file_csv = csv.writer(modif)
                    file_csv.writerow(row)
                    for row in orig_table:
                        csv.writer(modif)
                        file_csv.writerow(row)
    return file_modif + '.csv'
file = sys.argv[1]
divsum_splitter(file)
