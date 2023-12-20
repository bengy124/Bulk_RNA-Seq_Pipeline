# Bulk RNA-Seq Pipeline
Snakemake pipeline to automate the steps of QC, trimming, alignment, and quantification of NGS data. Utilizes sra toolkit, fasterq-dump, fastQC, fastp, Salmon and shell scripts to process and analyze fastq files.

## Usage
Run the shell script `obtain_fastq.sh` followed by an SRA accession number
```
./obtain_fastq.sh <SRA>
```
This will create a directory to prefetch the .sra files and then use fasterq-dump to acquire the fastq files


Next run `snakemake` with `-n` option to start a dry run to ensure everything is working then run with `-j` followed by the number of threads you want to utilize to begin the real run
```
# dry run
snakemake -s snakefile.py -n

# real run
snakemake -s snakefile.py -j threads
```
