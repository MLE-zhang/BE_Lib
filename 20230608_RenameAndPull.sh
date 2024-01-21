# change to directory where all fastq files are originally
cd 2023-08-02_819

# list the amplicons to be analyzed
amplicons=(TTTGTAGTCTAGTCT CATTATGATCGTACG CTATTCAGGGATTGA CTGATACCGGAAGAC ATCTCAGTTGAAGTG GTGTATACGACAGAG ACCGTGCACCTACCA AACCTCCTTAGTCTA AGTTCAGACCAATTG GTAGTTTGTCCAGAA CTCAGATTTTATCAC CAGAGGACGCACGCT CTACCTTTATGATCC TCCTTGGTCCTCGAG AAGAGGAGACGTCAG TCCAGATATCTTTAA CTAGTCTTTTGTAGT TCGTACGCATTATGA GGATTGACTATTCAG GGAAGACCTGATACC TGAAGTGATCTCAGT GACAGAGGTGTATAC CCTACCAACCGTGCA TAGTCTAAACCTCCT CCAATTGAGTTCAGA TCCAGAAGTAGTTTG TTATCACCTCAGATT GCACGCTCAGAGGAC ATGATCCCTACCTTT CCTCGAGTCCTTGGT ACGTCAGAAGAGGAG TCTTTAATCCAGATA)


#(a) rename each crispresso file with the name of the amplicon. I think I can sorta do this manually in the pre-treatment step

#iterate through this list and do:
#(1) Make a new folder on you local drive that has the amplicon name. Call this "Compile"
mkdir Compile
#(2) Copy the corresponding files into the local folder
#	-CRISPRessoBatch_quantification_of_editing_frequency.txt
#	-Nucleotide_percentage_summary.txt
#mv [name1] [name2]
#cp [directory1/name1] [directory2]

for folder in ${amplicons[*]}; do
	# create folder


	#cp CRISPRessoBatch_quantification_of_editing_frequency.txt 
	mkdir Compile/$folder
	pwd
	cp ./$folder/CRISPRessoBatch_on_batch_settings/CRISPRessoBatch_quantification_of_editing_frequency.txt ./Compile/$folder
	cp ./$folder/CRISPRessoBatch_on_batch_settings/Nucleotide_percentage_summary.txt ./Compile/$folder
	#cd Compile
	#mkdir $folder
	#cd folder
	#cp CRISPRessoBatch_quantification_of_editing_frequency.txt 
done



#----------------------------------
# iterate through this list and do: 1) create a new folder for each amplicon name,
# and 2) move all appropriate fastq files into that new folder
##for folder in ${amplicons[*]}; do
	# create folder
##	mkdir $folder
	# find all fastq files that contain the desired amplicon name as the first 
	# characters of their filename
##	for file in $( ls ${folder}-* ); do
		# move those files into the newly created folder one by one
##		mv $file ${folder}/${file}
##	done
##done

# iterate through the list of amplicons
##for folder in ${amplicons[*]}; do
	# change directory to the appropriate folder
##	cd $folder
	# create batch_settings.txt file with header
##	echo r1'\t'n > batch_settings.txt
	# populate batch_settings.txt file with info from all samples in folder
##	for sample in $( ls *.gz ); do
##		echo ${sample}'\t'${sample%?????????} >> batch_settings.txt
##	done
	# lookup sgRNA and amplicon sequence from database csv file
##	ga="$(python $(dirname $(dirname $PWD))/read_g+a_csv.py $folder)"
	# isolate guide and amplicon sequences separately
##	g="$(cut -d',' -f1 <<<"$ga")"
##	a="$(cut -d',' -f2 <<<"$ga")"
	# run CRISPRessoBatch
##	docker run -v ${PWD}:/DATA -w /DATA -i pinellolab/crispresso2 CRISPRessoBatch --batch_settings batch_settings.txt -g $g -a $a -w 20 -wc -10 -q 30 -p 2 --skip_failed --exclude_bp_from_left 5
	# move up one directory level out of the specific amplicon folder
##	cd ..
##done