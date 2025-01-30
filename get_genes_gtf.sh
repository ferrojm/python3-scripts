#!/bin/bash

if [ "$1" = "" ]
then
  echo "This script filters a gtf file by transcript IDs associated to a list of gene IDs"
  echo "Usage: $0 annotation.gtf list_genes_ids"
  exit 1
fi

# Remove original header, filter only transcripts, add gene number at the start and filter by occurrence
sed '1,3d' $1 | awk '$3 == "transcript" {print $10"-"$0}' | sed 's/"//; s/"//; s/;//' | sort | awk '!seen[$1]++' > tmp

echo '##gtf-version 3-filtered' > filtered_genes.gtf
grep -w -f $2 tmp >> filtered_genes.gtf
rm tmp
echo "-filtered_genes.gtf exported"
awk '{print $12}' filtered_genes.gtf | sed 's/"//g' | sed -E 's/\.[^.]*$|_[^_]*$//' > filtered_list.txt
echo '-filtered_list.txt exported'
