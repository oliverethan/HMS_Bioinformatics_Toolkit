# Ethan Oliver
# Harvard Medical School
# Department of Biomedical Informatics
# Park Lab
# 2019


# Runs SigMA on a CSV in both lite and full format
# Params: Input CSV

devtools::load_all()
args = commandArgs(trailingOnly=TRUE)
run(args[1], data ='msk', do_assign = T, tumor_type = 'breast', do_mva = T, lite_format = F, check_msi = T)
run(args[1], data ='msk', do_assign = T, tumor_type = 'breast', do_mva = T, lite_format = T, check_msi = T)
