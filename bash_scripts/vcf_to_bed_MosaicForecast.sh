
cat <(cat $1  |grep -v '^#'|grep -v str_contraction|grep -v t_lod_fstar|grep -v triallelic_site|cut -f1,2,4,5,10|sed \
's/:/\t/g'|sed 's/,/\t/g'|awk '$7>=3'|awk '$8>=0.03'|grep -v "0|1") <(cat $1 |grep -v '^#'|grep -v str_contraction|grep -v t_lod_fstar|grep -v triallelic_site|cut -f1,2,4,5,10|sed 's/:/\t/g'|sed 's/,/\t/g'|awk '$7>=3'|awk '$8>=0.02'|grep "0|1")|awk '$8<0.4'|awk '{OFS="\t";print $1,$2-1,$2,$3,$4,"BAM_NAME"}'



