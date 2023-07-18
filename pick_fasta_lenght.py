#!/usr/bin/python3

import sys, os
from Bio import SeqIO
import argparse

def manipulate_files(fasta):
    return fasta, "sampled_" + fasta

def achieve_lenght(fasta, lenght):
    total_number = 0
    sequence_number = 0
    original_file, sampled_file = manipulate_files(fasta)
    with open(original_file), open(sampled_file, "w") as sampled:
        for record in SeqIO.parse(original_file, "fasta"):
            if len(record.seq) >= lenght:
                SeqIO.write(record, sampled, "fasta")
                sequence_number += 1
            total_number += 1
    return total_number, sequence_number


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This script filters by lenght each record of a fasta file")
    parser.add_argument("-f", "--file", type=str, required=True, help="specify the fasta file", metavar="")
    parser.add_argument("-l", "--lenght", type=int, default=1, help="specify the minimun lenght that you want to filter", metavar="")
    
    args = parser.parse_args()
    fasta  = args.file
    lenght = args.lenght
    
    total_number, sequence_number = achieve_lenght(fasta,lenght)
    
        
    print(total_number, sequence_number) 
