# enceladus big data

## O que é?

**Enceladus Big Data** é um sistema criado para ajudar pesquisadores da **Sociedade Brasileira de Queimaduras (SBQ)** na coleta, processamento e distribuição de dados brutos em informações úteis por meio da linguagem R, Python e demais bibliotecas que auxiliam na manipulação dos registros.

## Colaboradores

Desenvolvido por: [José Inácio Rodrigues da Silva](https://github.com/josersinacio) e [Josué de Paulo Viana](https://github.com/josuepviana) 

Orientador: [Me. Fábio Ferraz Fernandez](http://lattes.cnpq.br/9386664812059696) 

Com a colaboração de: [Dr. Sérgio Eduardo Soares Fernandes](http://lattes.cnpq.br/9797758799188189)


## Como rodar:

**Instalar dependências primárias**

Python v3 (`sudo apt install python python-is-python3`)

Pip v3 (`sudo apt install python3-pip`)

Venv (`sudo apt install python3-venv`)

R (`sudo apt install r-base`)

OpenSSL (`sudo apt install libcurl4-openssl-dev libssl-dev`)

Pandoc (`sudo apt install pandoc`)

Texline (`sudo apt install texlive`)

Latex extras (`sudo apt install texlive-latex-extra`)

Libfonts (`sudo apt-get install libfontconfig1-dev`)

**Fazer clone do projeto do Github:**

    git clone git@github.com:josersinacio/EnceladusBigData.git

**Criar e habilitar  um VirtualEnv para o Python:**

	cd src
    python -m venv venv 
    source venv/bin/activate

**Instalar o wheel:**

    pip install wheel

**Instalar as dependências do requirements.txt**

    pip install -r requirements.txt

**Executar o setup.py que fará uma configuração básica para o python**

    sudo python setup.py

***P.S.:** setup.py fará um download de CSV contendo uma estimativa populacional de 2020 no formato state,state_ibge_code,city_ibge_code,city,estimated_population.
setup.py também instalará as biblioteca do R (incluindo o Microdatasus)*
