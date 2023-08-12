#!/usr/bin/python3
#stolen from @mylena-s XD

from Bio import SeqIO
import sys

def count_bases(file):
    '''counts the number of bases in all the sequences of a fasta file'''
    lenght=0
    for seq_record in SeqIO.parse(file, "fasta"):
        lenght= lenght + len(seq_record)
    print(lenght)

if __name__ == "__main__":
    try:
        file = sys.argv[1]
    except:
        print ("Usage: count_bases.py Fasta_file")   
    count_bases(file)
