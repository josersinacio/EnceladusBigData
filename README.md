# epidemiotcc
TCC - Mineração de Informações em Epidemiologia

![Diagrama principal](diagramas/fluxograma_principal.png)

## Integrantes
- [José Rodrigo da Silva Inácio](mailto:jose.inacio@estudante.ifb.edu.br)
- [Josué de Paulo Viana](mailto:josue.viana@estudante.ifb.edu.br)

### Atualizar a distro Linux utilizada

```bash
sudo apt update
sudo apt upgrade
```

## Setup Python

### Instalar GDAL (Necesário para PySUS)

```bash
sudo add-apt-repository -y ppa:ubuntugis/ubuntugis-unstable
sudo apt update
sudo apt upgrade
sudo apt-get install g++
sudo apt-get install python3-dev
sudo apt install gdal-bin libgdal-dev
```

### Instalar Venv

```bash
sudo apt install python3-venv
python3 -m venv ./venv
venv/Scripts/activate # Windows
source venv/bin/activate # Linux
pip install GDAL==$(gdal-config --version) --global-option=build_ext --global-option="-I/usr/include/gdal" 
pip install -r requirements.txt
```

### Exportar Venv - Req. Atualizados

```bash
pip freeze > requirements.txt
```

## SETUP R STUDIO

```bash
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
sudo add-apt-repository 'deb https://cloud.r-project.org/bin/Linux/ubuntu focal-cran40/'
sudo apt install -y r-base r-base-core r-recommended r-base-dev gdebi-core build-essential libcurl4-gnutls-dev libxml2-dev libssl-dev
wget https://rstudio.org/download/latest/stable/server/bionic/rstudio-server-latest-amd64.deb
sudo gdebi rstudio-server-latest-amd64.deb
```

### Executando um Exemplo

```bash
python poc/main.py

# Em outro terminal/aba
curl --location --request GET 'localhost:5000/diagramas/queimaduras?email=#EMAIL-CADASTRADO#&ano_inicio=2019&ano_fim=2019&estado=MT'
```

### Troubleshooting

#### Exemplo não rodou por falta do 'microdatasus'

```r
sudo rstudio-server start

#http://localhost:8787
#mesmo usuario e senha do linux

install.packages("remotes")
remotes::install_github("rfsaldanha/microdatasus")

sudo rstudio-server stop
```

#### Exemplo não rodou por falta de X pacote

```r
sudo rstudio-server start

#http://localhost:8787
#mesmo usuario e senha do linux

install.packages("#PACOTE QUE ESTIVER FALTANDO#")

sudo rstudio-server stop
```

