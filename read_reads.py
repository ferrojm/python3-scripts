#/usr/bin/python3

#read a fasta/fastq file and plot a histogram of length distribution


from Bio import SeqIO
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def read_reads(file, mode):
    sequences = []
    for seq_record in SeqIO.parse(file, mode):
        sequences.append(seq_record.seq)
    sizes = [len(rec) for rec in sequences]
    plt.hist(sizes, bins = 100)
    plt.xlabel('Seq length (bp)')
    plt.ylabel('Count')
    plt.show()
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser('plot a length histogram from a fasta o fastq file')
    parser.add_argument('-i', '--input', type = str, required = True, help = 'input file')
    parser.add_argument('-t', '--type', type = str, help = 'type of input fasta/fastq')
    args = parser.parse_args()
    file = args.input
    mode = args.type

read_reads(file, mode)
