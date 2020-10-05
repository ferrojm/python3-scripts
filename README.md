# Python3-scripts
Python3 scripts for working with NGS

## header_to_tab(fasta)
usage: <header_to_tab -i fasta>

Extract sequences headers from RMasker custom lib and generates a tab-separated custom_patter.csv list file like:
variant#sat/family <tab> family#sat/family
  
e.g.,
### input:

>R1CL1_A_sample1#sat/R1CL1_sample1  
sequence\
...\
>R1CL1_F_sample1#sat/R1CL1_sample1\
sequence\
...  

### output:

R1CL1_A_sample1#sat/R1CL1_sample1	R1CL1_sample1#sat/R1CL1_sample1\
...\
R1CL1_F_sample1#sat/R1CL1_sample1 R1CL1_sample1#sat/R1CL1_sample1\
...
