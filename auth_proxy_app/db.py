import logging

import redis


from auth_proxy_app.settings import auth_proxy_settings

redis_data = {
    "host": auth_proxy_settings.REDIS_HOST,
    "port": auth_proxy_settings.REDIS_PORT,
    "db": 0,
    "decode_responses": True
}
logging.info("Redis data: {redis_data}".format(redis_data=redis_data))
redis_db = redis.StrictRedis(**redis_data)
