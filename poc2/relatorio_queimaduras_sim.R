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


dados_processados = process_sim(big_data)

dados_processados = subset(dados_processados, DTOBITO> data_inicio & DTOBITO < data_fim)

print(names(dados_processados))

## DIAGRAMA DE LOCAL 

## TABELA DE CASOS POR CIDADE/MUNICIPIO

#soma o total de casos em cada municipio
dados_finais = dados_processados %>%                
  group_by(across(all_of(c("CODMUNRES", "munResNome")))) %>% 
  tally()   # Now summarise with unique elements 


projecao_populacional = read.csv("/home/josersi/projects/epidemiotcc/data/static/populacao-estimada-2020.csv")

projecao_populacional$city_ibge_code = as.character(projecao_populacional$city_ibge_code)
projecao_populacional$city_ibge_code <- substr(projecao_populacional$city_ibge_code, 1, 6)

dados_finais[["POPULACAO"]] <- NA
dados_finais[["DENSIDADE"]] <- NA
dados_finais[["UF"]] <- NA
dados_finais = filter(dados_finais, substr(CODMUNRES, 3, 6) != "0000")
dados_finais = as.data.frame(dados_finais)

print(head(projecao_populacional))

for(i in rownames(dados_finais)) {
  codigo_municipio = dados_finais[[i, "CODMUNRES"]]

  projecao = projecao_populacional[projecao_populacional$city_ibge_code == codigo_municipio, "estimated_population"]
    
  dados_finais[[i, "POPULACAO"]] = projecao
  dados_finais[[i, "DENSIDADE"]] = (dados_finais[[i, "n"]] / projecao) * 100000
}

dados_finais$DENSIDADE = formatC(dados_finais$DENSIDADE, format = "f", digits = 2, decimal.mark = ",")

dados_finais = dados_finais[, c("CODMUNRES", "munResNome", "POPULACAO", "n", "DENSIDADE")]
colnames(dados_finais) <- c("Código", "Município", "População*", "Casos", "por 100 mil hab.")


pdf(nome_arquivo, paper = "a4r", width = 9, height = 11.7)

# Divide as páginas a cada 24 registros
conjuntos <- split(dados_finais,seq(nrow(dados_finais)) %/% 24) 

for (conjunto in conjuntos) {
  row.names(conjunto) <- NULL
  grid.newpage() # Cria uma nova página
  grid.table(conjunto)
}

dev.off()

warnings()
