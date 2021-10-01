import redis
import pickle
from pysus.online_data.SIM import download

redisClient = redis.Redis('localhost')

def download_dataset(state, year):
    key = f'dataset-{state}-{year}'

    if redisClient.exists(key):
        print(f'{key} já armazenado.')

        return pickle.loads(redisClient.get(key))
    else:  
        value = download(state, year)

        print(f'Armazenando para {key}.')

        redisClient.set(key, pickle.dumps(value))
        return value