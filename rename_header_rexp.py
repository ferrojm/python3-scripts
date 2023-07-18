#!/usr/bin/python3
from Bio import SeqIO
import argparse
import os

####rename_description_rexp.py###

##Usage: rename_description_rexp.py -i fasta


##*rename headers id of a fasta file as "repeatname_variant_species#class/subclass" for creating a custom library for RepeatExplorer. 
##**check that headers lenght are < 50
##***check some possible misspellings

###NOMENCLATURE####
##1) input header: >repeatname_or_cLusternumber_variant_specimenorspeciesname. Variant characters lengh should be between 1 and 2 (e.g., _A_ or _1A_ or _23_).

###JMF > ferrojm@gmail.com



def change_header(original_file, class_i):
    print(class_i)
    class_i = "#" + class_i + "/"
    new_name = original_file.split(".")[0]
    duplicated_file = new_name + "_id_customRE.fasta"
    checkpoint = True
    with open(original_file) as original, open(duplicated_file, "w") as duplicated:  #open the input fasta
        for record in SeqIO.parse(original, "fasta"):
            record.description = ""     #delete the fasta description if it has one 
            if len(record.id.split("_")) > 3:  #the monomer is a variation and will take the original variant! (e.g., R2CL3_frog2_R1CL2_A_frog1)
                if (len(record.id.split("_")[-2]) != 1 and len(record.id.split("_")[-2]) != 2) or record.id[-1] == "_": #checks for possibles misspellings (includes HOR as 1A, 1B...)
                    print("\nCheck the monomer " + record.id + " for a possible misspelling or error!!!\n the monomer id was not changed")
                    checkpoint = False
                else:
                    record.id = record.id + class_i + record.id.split("_")[-3]+"_"+record.id.split("_")[-1] 
            else: #the monomer is new!! (e.g., R1CL2_A_frog1)
                record.id = record.id + class_i + record.id.split("_")[0]+"_"+record.id.split("_")[-1] 
            SeqIO.write(record, duplicated, "fasta")
            if len(record.id) > 49: #check the monomer lenght to be less than 50
                print("Check the record " + record.id + " final lenght!!")
                checkpoint = False
        duplicated.close()
       
        #os.system("sed -i 's/>//g' " + duplicated_file) #activate this to delete the ">" symbol
    if checkpoint:
        print("""\nfasta was correctly modified with the name:\n""",">",duplicated_file)
    else:
        os.system("rm "+ duplicated_file)
        print("\nFile was not created due to listed errors!!!")
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "rename headers id of a fasta file as name#sat/name. Usage rename_description_rexp.py -i fasta\n. By default it adds #sat/ class. Optionally use -c and the string to add")
    parser.add_argument("-i", "--input", type = str, required = True, help = "file input")
    parser.add_argument("-c", "--class_input", type = str, help = "add a class string")
    args = parser.parse_args()
    original_file = args.input
    class_i = args.class_input
    if class_i == None:
        class_i = 'sat'

change_header(original_file, class_i)  
