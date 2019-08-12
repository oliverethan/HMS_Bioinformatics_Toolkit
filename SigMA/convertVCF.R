# Ethan Oliver
# Harvard Medical School
# Department of Biomedical Informatics
# Park Lab
# 2019

# Converts VCFs to  96 dim CSV for SigMA analysis
# Params: Input directory, Output file name

library(ggplot2) 
devtools::load_all()

args = commandArgs(trailingOnly=TRUE)

if (length(args) < 2) {
  stop("At least two argument must be supplied: Input directory, Output file name", call.=FALSE)
}

print("make_matrix")
m <- make_matrix(args[1], file_type = 'vcf', ref_genome = )
print("conv_snv_matrix_to_df")
df <- conv_snv_matrix_to_df(m)


write.table(df, paste('<FULL_PATH>', args[2], '.csv', sep="") , row.names = F, sep = ',', quote = F)