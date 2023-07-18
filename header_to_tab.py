#!/usr/bin/python3

from Bio import SeqIO
import argparse
def header_to_tab(original_file):
	new_name = original_file.split(".")[0]
	modified_file = new_name + ".csv" #create a csv file
	lista_records = list()
	with open(original_file) as original, open(modified_file, "w") as modified: #open input fasta
		for record in SeqIO.parse(original, "fasta"):
			record.description = ""
			splited = record.id.split("/")
			record.id = record.id + "\t" + splited[1] + "#sat/" + splited[1]
			lista_records.append(record.id)

		for record in lista_records:
			modified.write(record + "\n")
		

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = "<header_to_tab -i fasta> extract sequences headers from RMasker lib and generates a tab separated record like var#sat/fam <tab> fam#sat/fam")
	parser.add_argument("-i", "--input", type = str, required = True, help = "a fasta input")
	args = parser.parse_args()
	original_file = args.input
	header_to_tab(original_file)
