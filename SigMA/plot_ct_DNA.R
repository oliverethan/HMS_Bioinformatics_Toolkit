# Ethan Oliver
# Harvard Medical School
# Department of Biomedical Informatics
# Park Lab
# 2019

# Plots ct_DNA_table

library(ggplot2) 
source('R/plot_tribase_dist.R')

df <- read.csv('ct_DNA_table.csv')

for(row in 1:nrow(df)){
        tumorname = df[row, "tumor"]
        day = df[row, "DaysFromPreTreatment"]
        print("TUMOR NAME: ")
        print(tumorname)
        plot <- plot_tribase_dist(as.data.frame(t(df[df$tumor == tumorname, 1:96])), signame = paste(tumorname, " Day: ", day ))
        ggsave(plot, file = paste('output/normal/', tumorname, '.pdf',sep=""), width = 6, height = 2)
}