#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 12:21:39 2021

@author: ferrojm@gmail.com
"""
import argparse
import os
from Bio import SeqIO

"""
Dependencies

Seqkit (https://github.com/kwongj/fa-mask)
Biopython (https://biopython.org/wiki/Packages)

"""
"""
Usage:
   pcr_main.py [option] target.fasta <other arguments> 

Options:
-m    mode (pcr, mpcr, N)

Arguments:
-t    target fasta to amplify (required) 
-f    forward primer
-r    reverse primer
-p    path for multi-pcr
-q    query sequence to search within a target by id 
-o    output name (optional)
"""
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, 
                                 description="script to do a pcr in silico in one (pcr mode) or multiple files (mpcr mode), also search an exact match in a target and replace nucleotides with N (N mode)",
                                 usage="\npcr_main.py -m mode target.fasta <other arguments>\n#single pcr: -m pcr -t input.fasta -f primer_f -r primer_r\n#a batch pcr(all .fasta files in a directory): -m mpcr -p path_of_fasta -f primer_f -r primer_r\n#search a seq within another, if there is a match replace the sequence by 'Ns': -m N -t target.fasta -q query.fasta")
parser.add_argument("--mode", "-m", type = str, required = True, help= "mode (pcr, mpcr, N")
parser.add_argument("--target", "-t", help ="target fasta to amplify")
parser.add_argument("--forward", "-f", help ="forward primer")
parser.add_argument("--reverse", "-r", help ="reverse primer")
parser.add_argument("--path", "-p", type = str, help = "path to fasta files")
parser.add_argument("--query", "-q", help ="query sequence to search within a target by id")
#parser.add_argument("--output", "-o", default = "pcr_output", help = "output name (optional)")                    

"""
takes an input and a pair of primers 
and get an in-silico amplicon using seqkit
"""

def pcr_single(fasta, primerF, primerR):
    output = fasta.split(".")[0] + "_output.fa"
    output_pcr = os.system("seqkit amplicon " + fasta + " -F " + primerF + " -R " + primerR + " > " + output)
    os.system("echo '' &&"+ "cat " + output)
    print("")
    print("### The output was saved as ", output, " ###")
    return output_pcr


"""
for multiple fasta files within a directory
"""

def pcr_mutiple(path, primerF, primerR, output):
    path = path + "/*.fasta"
    return pcr_single(path, primerF, primerR, output)    


"""
uses as input a short sequence(query) and a longer sequence (target).
Searches the query by id and replace the match by a N (yet)
"""

def pcr_replace(fasta, sequence):
    with  open(fasta,"r") as fa, open(sequence, "r") as sq, open("output_Nreplaced_" + ".fasta", "w") as out:
        record_target = SeqIO.to_dict(SeqIO.parse(fa, 'fasta'))
        for record_query in SeqIO.parse(sq, "fasta"):
            if record_query.id in record_target:
                record_target_new = record_target[record_query.id]
                record_query_inicio = record_target_new.seq.find(record_query.seq) #inicio de la seq en el fasta
                record_query_final = record_query_inicio + len(record_query.seq)    #final de la seq en el fasta
                newseq = (record_target_new.seq).tomutable()
                newseq[record_query_inicio:record_query_final] = "N"*len(record_query.seq)
                record_target_new.seq = newseq
                SeqIO.write(record_target_new, out, "fasta") 
            
        print("The output was saved as output_Nreplaced_.fa")

"""
Main Function
"""
if __name__ == '__main__':
    args = parser.parse_args()
    mode = args.mode
    target = args.target
    forward = args.forward
    reverse = args.reverse
    path = args.path
    query = args.query
#    output = args.output
    
    if mode == "pcr":
        pcr_single(target, forward, reverse)
        
    elif mode == "mpcr":
        pcr_mutiple(path, forward, reverse, "Mpcr_output")
        print("The output was saved as Mpcr_output.fa")
                 
    elif mode == "N":
        pcr_replace(target, query)