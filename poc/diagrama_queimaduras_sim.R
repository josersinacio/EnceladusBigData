library(microdatasus)
library(dplyr)
library(stringi)
library(stringr)
library(gridExtra)
library(grid)
library(lubridate)
library(plyr)

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

datalist <- list()

for (i in 1:length(estados)) {
  dados <- fetch_datasus(
    year_start = ano_inicio, 
    year_end = ano_fim, 
    uf = estados[[i]], 
    information_system = "SIM-DO")
  
  dados_filtrados <- filter(dados, str_detect(CAUSABAS, regex) | str_detect(CAUSABAS_O, regex))
  
  datalist[[i]] <- dados_filtrados
}


big_data  <- bind_rows(datalist)

dados_processados <- process_sim(big_data)

## DIAGRAMA DE LOCAL 

ocorrencias <- as.data.frame(t(table(dados_processados$LOCOCOR)))

colors <- rainbow(length(ocorrencias$Freq))

pdf(nome_arquivo, paper = "a4r", width = 8.3, height = 11.7)

pie(ocorrencias$Freq, labels = ocorrencias$Freq, col = colors)

legend("topleft", legend = ocorrencias$Var2, fill = colors)

## TABELA DE CASOS POR CIDADE/MUNICIPIO

# Isola os nomes de municipios
municipios <- unique(dados_processados$munResNome)

#soma o total de casos em cada municipio
dados_finais <- setNames(
  aggregate(
    x = as.integer(dados_processados$ORIGEM), # Base para contador (agregando)
    by = list(dados_processados$munResNome), # Identifica o que está duplicado
    FUN = sum),
  c("Municipio", "Total")) # Nomeia as colunas

meses = c("Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez")

for (mes in meses) {
  dados_finais[[mes]] <- vector(length = nrow(dados_finais))
}


for(i in 1:nrow(dados_finais)) {
  municipio <- dados_finais[i,]
  
  regex <- "\\d{4}-01-\\d{2}"
  
  for (i in 1:12) {
    mes <- meses[[i]]
  
    
    dados_finais[dados_finais$Municipio == municipio$Municipio, mes] <- nrow(
      dados_processados %>%
        filter(munResNome == municipio$Municipio & as.numeric(strftime(DTOBITO, "%m")) == i))
  }
  
}

# Cria header com o nome das colunas
dados_finais <- dados_finais[, c("Municipio", meses, "Total")]


# Divide as paginas a cada 22 registros
conjuntos <- split(dados_finais,seq(nrow(dados_finais)) %/% 24) 

for (conjunto in conjuntos) {
  grid.newpage() # Cria uma nova página
  grid.table(conjunto)
}

dev.off()
