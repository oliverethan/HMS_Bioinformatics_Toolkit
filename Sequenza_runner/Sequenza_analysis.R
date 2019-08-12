# Ethan Oliver
# Harvard Medical School
# Department of Biomedical Informatics
# Park Lab
# 2019

library(sequenza)
library(tools)


args = commandArgs(trailingOnly=TRUE)

if (length(args)==0) {
  stop("At least one argument must be supplied (input file)", call.=FALSE)
}

fname <- file_path_sans_ext(args[1])
print(fname)

test <- sequenza.extract(args[1], verbose = FALSE)

dir.create(fname)

CP <- sequenza.fit(test)
sequenza.results(sequenza.extract = test,
    cp.table = CP, sample.id = fname,
    out.dir=fname)
