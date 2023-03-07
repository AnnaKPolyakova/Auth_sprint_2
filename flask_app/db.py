import redis
from flask_sqlalchemy import SQLAlchemy

from flask_app.settings import settings

db = SQLAlchemy()

redis_db = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=True
)
