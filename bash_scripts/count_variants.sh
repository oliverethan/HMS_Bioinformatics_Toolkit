
for d in *.vcf ; do
    #python3 /n/data1/hms/dbmi/park/alon/command_line_tools/PreProcessing/PreProcessing_new.py -in_dir "$d" -out "$d"
    #echo "DIRECTORY"mee
    echo $d
    gatk CountVariants --verbosity ERROR --QUIET true \
      -V $d
done