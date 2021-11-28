import urllib.request
import os

dir = './data/static'

os.makedirs(dir, exist_ok=True)

urllib.request.urlretrieve(
    "https://enceladus-big-data.s3.us-east-2.amazonaws.com/populacao-estimada-2020_2020-08-27.csv", f"{dir}/populacao-estimada-2020.csv")
