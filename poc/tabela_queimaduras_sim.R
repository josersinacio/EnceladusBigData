library(microdatasus)
library(dplyr)
library(stringi)
library(stringr)

args <- commandArgs(TRUE)

estados = strsplit(args[[1]], ",")
ano_inicio <- args[[2]]
ano_fim <- args[[3]]
nome_arquivo <- args[[4]]

codigos = c(
  # Elétrica
  "W85", "W86", "W87", "X33", 
    
  # Calor/Térmica
  "W35", "W36", "W38", "W39", "W40", "W92", "X00", "X01", "X02", 
  "X03", "X04", "X05", "X06", "X08", "X09", "X10", "X11", "X12", 
  "X13", "X14", "X15", "X16", "X17", "X18", "X19", "X30", "X75", 
  "X76", "X77", "X88", "X96", "X97", "X98", "Y25", "Y26", "Y27", 

  # Química  
  "X86",

  # Outros (geladura, radiação)
  "W88", "W89", "W90", "W91", "W93", "X31", "X32"
)

regex <- stri_paste(codigos, collapse='|')


datalist = list()

for (i in 1:length(estados)) {
  dados <- fetch_datasus(
    year_start = ano_inicio, 
    year_end = ano_fim, 
    uf = estados[[i]], 
    information_system = "SIM-DO")
  
  dados_filtrados <- filter(dados, str_detect(CAUSABAS, regex) | str_detect(CAUSABAS_O, regex))
  
  datalist[[i]] <- dados_filtrados
}


big_data<- bind_rows(datalist)

dados_processados <- process_sim(big_data)

# Deleta colunas se completamente preenchidas por 'NA'
dados_finais <- dados_processados[, colSums(is.na(dados_processados)) < nrow(dados_processados)]

# Retorna tabela de todos os registros com base na limpeza feita previamente
write.csv(dados_finais, nome_arquivo)