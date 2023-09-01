import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv('.env'))
load_dotenv(find_dotenv('secrets.env'))

REDIS_HOST = ''
REDIS_PORT = 0
REDIS_PASSWORD = ''

try:
    REDIS_HOST = os.environ['REDIS_HOST']
except:
    raise Exception('Provide REDIS_HOST')

try:
    REDIS_PORT = int(os.environ['REDIS_PORT'])
except:
    raise Exception('Provide REDIS_PORT (integer)')

try:
    REDIS_PASSWORD = os.environ['REDIS_PASSWORD']
except:
    raise Exception('Provide REDIS_PASSWORD')

