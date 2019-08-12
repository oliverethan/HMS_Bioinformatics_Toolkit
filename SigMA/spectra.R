# Ethan Oliver
# Harvard Medical School
# Department of Biomedical Informatics
# Park Lab
# 2019


# Combines two SigMA outputs and plots the average Spectra of each call
# Params: Full input, Lite input

library(ggplot2) 
source('R/plot_tribase_dist.R')


args = commandArgs(trailingOnly=TRUE)
if (length(args)==0) {
  stop("At least two argument must be supplied  Full input, Lite input", call.=FALSE)
}



df1 <- read.csv(args[1])
df2 <- read.csv(args[2])
df_comb <- cbind(df1, df2[match(df1$tumor, df2$tumor),])
categories <- unique(as.character(df_comb$categ))
print(categories)

for(cat in categories){
        print(cat)
        plot <- plot_tribase_dist(as.data.frame(colMeans(df_comb[df_comb$categ == cat, 1:96])), signame = cat)
        ggsave(plot, file = paste('/n/data1/hms/dbmi/park/ethan/GERBURG/SIGMA_new/gerburg_10_vaf_2/', cat, '.pdf',sep=""), width = 6, height = 2)
}

