# Base Editor Profiling Library in E. coli
Code for processing data from base editing profiling

System requirements:  
Tested with python3 environment

Installation guide:  
Packages to install: seqkit, csv, pandas, os, glob, re, sys  
Typical install time: 10 minutes  

Demo:
Follow instructions below with the input fastq files provided.  Note that these fastq files have already been processed with the following code: 

seqkit seq -m 110 input.fastq.gz > output.fastq.gz

Expected output: BE_quant_AtoG_pos6.xlsx and BE_quant_CtoT_pos6.xlsx files   
Typical run time: 20 min

Instructions for use:  
First, process every input fasta with the following code:

seqkit seq -m 110 input.fastq.gz > output.fastq.gz

Then, split each output.fastq based on the barcode region using the following code:

seqkit output.fastq.gz -r 91:105

Next, copy the largest 32 files for the position 6 library or the largest 448 files for the positions 1-14 library into a new folder.  Run CRISPResso2 on these resulting fastq files.

From the same folder, run 20230608_RenameAndPull.sh to create a folder that compiles the necessary files for subsequent analysis.

Transfer the “Compile” folder into a new folder and run:

python BE+indels_quant_Library_try2.py #YourFolder# #OriginalBase# #FinalBase# #PositioninProtospacer#

Example for checking C to T editing at position 6 in the protospacer: python BE+indels_quant_Library_try2.py #YourFolder# C T 6

Note that the directories within the script will need to be changed to your current directories.

