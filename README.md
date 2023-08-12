# Python3-scripts
general python scripts and tools for working with NGS data

<code>AnalyzeLandscapes_v2.py</code>-plot repetitive landscapes using a RepeatMasker divsum output (AnalyzeLandscapes_v2.py -h for options).

<code>pick_fasta_lenght.py -f <file.fasta> -l <int_length> </code>- filters sequences keeping those above a desired length
  
<code>rename_header_rexp.py -i <file.fasta> </code>- Rename headers id of a fasta file as "name#sat/name" for using as a custom library for RepeatExplorer (Rmasker), also checks headers lenght (< 50) and possible misspellings

<code>pcr_main.py -t <target.fasta> -f <forward_primer_string> -r <reverse_primer_string> -m <modes= pcr, mpcr, N> </code>- PCR in silico from a template using seqkit, extract a PCR product from one (pcr mode) or multiple files (mpcr mode), also search an exact match in a target and replace nucleotides with N (N mode)

<code>count_bases.py </code> - counts the number of bases in all the sequences of a fasta file. made by: @mylena-s 


