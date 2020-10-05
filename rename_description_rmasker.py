#!/usr/bin/python3
from Bio import SeqIO
import argparse
import os

####rename_description_rmasker.py###

##Usage: rename_description_rmasker.py -i fasta


##*renames headers id of a fasta file for using as "name#sat/name" for using as a custom library for RepeatMasker. 
##**check header lenght (< 50)
##***check misspellings

###NOMENCLATURE####
##1) RoundCLusterNumber_Variant_SpecimenName. Variant characters lengh should be of 1 or 2.
##2) For variants found in two or more specimens: RoundCLusterNumber_Sp2_RoundCLusterNumber_Variant_Sp1
#### e.g.,  >R3CL200_SP2_R1CL224_D_SP1 -->> >R3CL200_SP2_R1CL224_D_SP1#sat/R1CL224_SP1

###JMF > ferrojm@gmail.com



def change_header(original_file):
    new_name = original_file.split(".")[0]
    duplicated_file = new_name + "_id_rmasker.fasta"
    checkpoint = True
    with open(original_file) as original, open(duplicated_file, "w") as duplicated:  #open the input fasta
        for record in SeqIO.parse(original, "fasta"):
            record.description = ""     #delete the fasta description 
            if len(record.id.split("_")) > 3:  #the monomer is a variation and will take the original sat! (e.g., R2CL3_frog2_R1CL2_A_frog1)
                if (len(record.id.split("_")[-2]) != 1 and len(record.id.split("_")[-2]) != 2) or record.id[-1] == "_": #checks for possibles misspellings (includes HOR as 1A, 1B...)
                    print("\nCheck the monomer " + record.id + " for a possible misspelling or error!!!\n the monomer id was not changed")
                    checkpoint = False
                else:
                    record.id = record.id + "#sat/" + record.id.split("_")[-3]+"_"+record.id.split("_")[-1] 
            else: #the monomer is new!! (e.g., R1CL2_A_frog1)
                record.id = record.id + "#sat/" + record.id.split("_")[0]+"_"+record.id.split("_")[-1] 
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
    parser = argparse.ArgumentParser(description = "rename headers id of a fasta file as name#sat/name. Usage rename_description_rmasker.py -i fasta")
    parser.add_argument("-i", "--input", type = str, required = True, help = "file input")
    args = parser.parse_args()
    original_file = args.input
    change_header(original_file)

