#!/usr/bin/bash

#Script to prepare salmon decoy.txt for indexing

dir=$1

#Creating directory
echo "Creating directory $dir"
mkdir -p $dir

#Obtaining assembly fasta file and transcript fasta file
echo "Downloading files..."
wget https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/latest_release/gencode.v44.pc_transcripts.fa.gz -P ./$dir
wget https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/latest_release/GRCh38.primary_assembly.genome.fa.gz -P ./$dir


#Preparing metadata 
echo "Preparing metadata..."
grep "^>" <(gunzip -c ./$dir/GRCh38.primary_assembly.genome.fa.gz) | cut -d " " -f 1 > ./$dir/decoys.txt
sed -i -e 's/>//g' ./$dir/decoys.txt
cat ./$dir/gencode.v44.pc_transcripts.fa.gz ./$dir/GRCh38.primary_assembly.genome.fa.gz > ./$dir/genome.fa.gz
echo "Done!"