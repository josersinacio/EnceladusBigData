import urllib.request
import os
import re

dir = './data/static'

os.makedirs(dir, exist_ok=True)

urllib.request.urlretrieve(
    "https://enceladus-big-data.s3.us-east-2.amazonaws.com/populacao-estimada-2020_2020-08-27.csv", f"{dir}/populacao-estimada-2020.csv")

def walk_through_files(path, file_extension='.R'):
   for (dirpath, dirnames, filenames) in os.walk(path):
      for filename in filenames:
         if filename.endswith(file_extension): 
            yield os.path.join(dirpath, filename)

for scriptFilename in walk_through_files('./rscripts'):
   with open(scriptFilename) as scriptFilename:
      for line in scriptFilename.readlines():
         if line .startswith('library('):
            libraryName = re.sub(r'library\((.*)\)', r'\1', line).strip()

            if (libraryName != 'microdatasus'):
               os.system(f'Rscript -e \'install.packages("{libraryName}")\'')

os.system('Rscript -e \'install.packages("remotes")\'')
os.system('Rscript -e \'install.packages("kableExtra")\'')
os.system('Rscript -e \'remotes::install_github("rfsaldanha/microdatasus")\'')