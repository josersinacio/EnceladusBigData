library(microdatasus)
library(dplyr)

args <- commandArgs(TRUE)

estados = strsplit(args[[1]], ",")
ano_inicio <- args[[2]]
ano_fim <- args[[3]]
codigos <- strsplit(args[[4]], ",")
nome_arquivo <- args[[5]]


for (i in 1:length(estados)) {
  dados <- fetch_datasus(
    year_start = ano_inicio, 
    year_end = ano_fim, 
    uf = estados[[i]], 
    information_system = "SIM-DO")
  
  dados_filtrados <- filter(dados, CAUSABAS %in% c('W85', 'W86', 'W87', 'X33') | CAUSABAS_O %in% c('W85', 'W86', 'W87',  'X33'))
  
  dados_processados <- process_sim(dados_filtrados)
  
  dados_processados <- select(dados_processados, -1)
  
  write.table(dados_processados, nome_arquivo, sep = ",", col.names = i == 1, row.names = FALSE, append = i > 1)
}


