#!/usr/bin/env python3

import os
import glob

SRA,FRR = glob_wildcards("rawReads/{sra}_{frr}.fastq")

rule all:
    input:
        #raw fastqc
        expand("rawQC/{sra}_{frr}_fastqc.{extension}", sra = SRA, frr = FRR, extension=["zip","html"]),      
        #fastp
        expand("trimmedReads/{sra}_1.trimmed.fastq", sra = SRA),
        expand("trimmedReads/{sra}_2.trimmed.fastq", sra = SRA),
        #trimmed fastqc
        expand("trimmedQC/{sra}_{frr}.trimmed_fastqc.{extension}", sra = SRA, frr = FRR, extension=["zip","html"]),
        #decoy
        "ref_genome/decoys.txt",
        "ref_genome/genome.fa.gz",
        #salmon index
        "salmon_index/",
        #salmon
        expand("salmon/{sra}/", sra = SRA)

rule rawFastqc:
    input:
        rawread = "rawReads/{sra}_{frr}.fastq"
    output:
        zip = "rawQC/{sra}_{frr}_fastqc.zip",
        html = "rawQC/{sra}_{frr}_fastqc.html"
    threads:
        1
    params:
        dir = "rawQC/"
    priority:
        6
    shell:
        "mkdir -p {params.dir} && fastqc {input.rawread} -t {threads} -o {params.dir}"

rule fastp:
    input:
        fastpread1 = "rawReads/{sra}_1.fastq",
        fastpread2 = "rawReads/{sra}_2.fastq"
    output:
        trimmed1 = "trimmedReads/{sra}_1.trimmed.fastq",
        trimmed2 = "trimmedReads/{sra}_2.trimmed.fastq"
    threads:
        20
    params:
        front = "15",
        tail = "15",
        dir = "trimmedReads/"
    priority:
        5
    shell:
        "mkdir -p {params.dir} && fastp -i {input.fastpread1} -I {input.fastpread2} -o {output.trimmed1} -O {output.trimmed2} -w {threads} -f {params.front} -t {params.tail}"
        
rule trimmedFastqc:
    input:
        trimmedread = "trimmedReads/{sra}_{frr}.trimmed.fastq"
    output:
        zip = "trimmedQC/{sra}_{frr}.trimmed_fastqc.zip",
        html = "trimmedQC/{sra}_{frr}.trimmed_fastqc.html"
    threads:
        1
    params:
        dir = "trimmedQC/"
    priority:
        4
    shell:
        "mkdir -p {params.dir} && fastqc {input.trimmedread} -t {threads} -o {params.dir}"

rule decoys:
    output:
        genome = "ref_genome/genome.fa.gz",
        decoys = "ref_genome/decoys.txt"
    priority:
        10
    params:
        dir = "ref_genome"
    shell:
        "./salmon_decoys.sh {params.dir}"

rule salmon_index:
    input:
        genome = "ref_genome/genome.fa.gz",
    output:
        directory("salmon_index/")
    threads:
        20
    params:
        decoys = "ref_genome/decoys.txt"
    priority:
        9
    shell:
        "mkdir -p {output} && salmon index -t {input.genome} -d {params.decoys} -i {output} -p {threads} --gencode" 

rule salmon:
    input:
        read1 = rules.fastp.output.trimmed1,
        read2 = rules.fastp.output.trimmed2,
    output:
        directory("salmon/{sra}/")
    threads:
        20
    params:
        index = rules.salmon_index.output,
        libtype = "A"
    priority:
        0
    shell:
        "mkdir -p {output} && salmon quant -i {params.index} -l {params.libtype} -1 {input.read1} -2 {input.read2} -p {threads} -o {output}"
