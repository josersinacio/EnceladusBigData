library(dplyr)
library(stringi)
library(stringr)
library(janitor)
require(rmarkdown)
library(microdatasus)


args <- commandArgs(TRUE)

estado <- args[[1]]
data_inicio <- as.Date(args[[2]])
data_fim <- as.Date(args[[3]])
nome_arquivo <- args[[4]]


ano_inicio <- strftime(data_inicio, "%Y")
ano_fim <- strftime(data_fim, "%Y")

codigos_causa_eletrica <- c("W85", "W86", "W87", "X33");
codigos_causa_calor_e_termica <- c(
  "W35", "W36", "W38", "W39", "W40", "W92", "X00", "X01", "X02",
  "X03", "X04", "X05", "X06", "X08", "X09", "X10", "X11", "X12",
  "X13", "X14", "X15", "X16", "X17", "X18", "X19", "X30", "X75",
  "X76", "X77", "X88", "X96", "X97", "X98", "Y25", "Y26", "Y27"
)
codigos_causa_quimica <- c("X86");
codigos_causa_gelad_e_rad <- c(
  "W88", "W89", "W90", "W91", "W93", "X31", "X32"
)

codigos <- c(
  # Elétrica
  codigos_causa_eletrica,
  # Calor e Térmica
  codigos_causa_calor_e_termica,
  # Química
  codigos_causa_quimica,
  # Outros (geladura, radiação)
  codigos_causa_gelad_e_rad
)

regex <- stri_paste(codigos, collapse = "|")


dados <- fetch_datasus(
  year_start = ano_inicio,
  year_end = ano_fim,
  uf = estado,
  information_system = "SIM-DO"
)

big_data <- subset(dados,
  str_detect(CAUSABAS, regex) | str_detect(CAUSABAS_O, regex)
)

dados_processados <- process_sim(big_data) %>%
  janitor::clean_names()

dados_processados <- subset(dados_processados,
  as.Date(dtobito) > data_inicio
    & as.Date(dtobito) < data_fim
    & substr(codmunres, 3, 6) != "0000"
)


## DIAGRAMA DE LOCAL

## TABELA DE CASOS POR CIDADE/MUNICIPIO

# soma o total de casos em cada municipio
municipios_com_casos <- dados_processados %>%
  group_by(across(all_of(c("codmunres", "mun_res_nome")))) %>%
  tally() # Now summarise with unique elements

projecao_populacional <- read.csv("./data/static/populacao-estimada-2020.csv")

projecao_populacional$city_ibge_code <- as.character(
  substr(projecao_populacional$city_ibge_code, 1, 6)
)

municipios_com_casos$populacao <- NA
municipios_com_casos$densidade <- NA

municipios_com_casos <- as.data.frame(municipios_com_casos)


for (i in rownames(municipios_com_casos)) {
  codigo_municipio <- municipios_com_casos[[i, "codmunres"]]

  projecao <- projecao_populacional[
    projecao_populacional$city_ibge_code == codigo_municipio,
    "estimated_population"
  ]

  municipios_com_casos[[i, "populacao"]] <- projecao
  municipios_com_casos[[i, "densidade"]] <- (
    municipios_com_casos[[i, "n"]] / projecao) * 100000
}

municipios_sem_casos <- projecao_populacional[
  !(projecao_populacional$city_ibge_code %in% municipios_com_casos$codmunres),
, ]

municipios_sem_casos <- municipios_sem_casos[
  municipios_sem_casos$state == estado,
  c("city", "estimated_population")
]

rownames(municipios_sem_casos) <- seq.int(nrow(municipios_sem_casos))

municipios_com_casos <- municipios_com_casos[,
  c("mun_res_nome", "populacao", "n", "densidade")
]

write.csv(
  municipios_com_casos,
  "poc2/municipios_com_casos.csv"
)

write.csv(
  municipios_sem_casos,
  "poc2/municipios_sem_casos.csv",
  row.names = FALSE
)

rmarkdown::render("poc2/relatorio_queimaduras.Rmd",
  output_file = nome_arquivo,
  params = list(
    dt_inicio = data_inicio,
    dt_fim = data_fim,
    uf = estado
  )
)