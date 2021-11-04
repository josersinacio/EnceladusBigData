library(microdatasus)
library(plyr)
library(dplyr)
library(stringi)
library(stringr)
library(gridExtra)
library(grid)
library(lubridate)


estado = "MA"
data_inicio = as.Date("2017-08-01")
data_fim = as.Date("2019-08-30")
nome_arquivo = "~/.enceladus/temp.pdf"


ano_inicio = strftime(data_inicio, "%Y")
ano_fim = strftime(data_fim, "%Y")

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


dados <- fetch_datasus(
    year_start = ano_inicio, 
    year_end = ano_fim, 
    uf = estado, 
    information_system = "SIM-DO")
  
big_data <- filter(dados, str_detect(CAUSABAS, regex) | str_detect(CAUSABAS_O, regex))


dados_processados <- process_sim(big_data)

dados_processados <- subset(dados_processados, DTOBITO> data_inicio & DTOBITO < data_fim)

print(names(dados_processados))

## DIAGRAMA DE LOCAL 

pdf(nome_arquivo, paper = "a4r", width = 9, height = 11.7)

## TABELA DE CASOS POR CIDADE/MUNICIPIO

#soma o total de casos em cada municipio
dados_finais <- setNames(
  aggregate(
    x = as.integer(dados_processados$ORIGEM), # Base para contador (agregando)
    by = list(dados_processados$CODMUNRES), # Identifica o que está duplicado
    FUN = sum),
  c("CODMUNRES", "Total")) # Nomeia as colunas

foo <- function(cod){which(CODMUNRES == cod)[1]}

dados_finais[["Município"]] <- apply(dados_processados, dados_finais$CODMUNRES, foo)[["munResNome"]]

# Divide as páginas a cada 24 registros
conjuntos <- split(dados_finais,seq(nrow(dados_finais)) %/% 24) 

for (conjunto in conjuntos) {
  row.names(conjunto) <- NULL
  grid.newpage() # Cria uma nova página
  grid.table(conjunto)
}

dev.off()

