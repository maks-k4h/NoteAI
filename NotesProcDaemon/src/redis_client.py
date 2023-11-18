import os
from dotenv import find_dotenv, load_dotenv

import redis


load_dotenv(find_dotenv('.env'))
load_dotenv(find_dotenv('secrets.env'))

r = redis.Redis(
    host=os.environ['REDIS_HOST'],
    port=os.environ['REDIS_PORT'],
    password=os.environ['REDIS_PASSWORD'],
    decode_responses=True
)

if not r.exists('npd'):
    r.xadd('npd', {'uuid': '', 'channel': ''})


