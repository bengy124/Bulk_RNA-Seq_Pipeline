#!/usr/bin/bash

#Script to prefetch SRAs and obtain fastq files

SRA=$1
dir='rawReads'

#Prefetching SRAs
echo "Creating directory..."
mkdir $dir
echo "Beginning prefetch..."
prefetch $SRA -O $dir
echo "Prefetch complete!"

#Tidying directory
echo "Cleaning directory..."
find $dir -name "*.sra" -type f -exec mv {} $dir \;
find $dir -type d -empty -delete
echo "Directory cleaned!"

#Obtaing fastq files from SRAs
echo "Beginning fasterq-dump..."
for sra_file in $dir/*.sra; do fasterq-dump $sra_file --threads 20  -O $dir; done
echo "Obtained fastq files!"

#Moving SRAs to new folder
echo "Moving SRA files..."
mkdir $dir/$SRA
mv $dir/*.sra $dir/$SRA 
echo "Moved SRA files to $dir/$SRA!"