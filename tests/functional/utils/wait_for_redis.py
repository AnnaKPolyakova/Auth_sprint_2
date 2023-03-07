import logging
import time

import redis

from tests.functional.settings import test_settings

if __name__ == '__main__':
    host = test_settings.REDIS_HOST
    port = test_settings.REDIS_PORT
    redis_client = redis.Redis(host=host, port=port, db=0)
    while True:
        if redis_client.ping():
            logging.info("Successfully connected to redis")
            break
        time.sleep(1)
