from redis import Redis
from flask import current_app

redis = Redis(host=current_app.config['CACHE_HOST'], port=current_app.config['CACHE_PORT'], decode_responses=True, ssl=True)

class RedisClient:
    def __init__(self):
        self.redis = redis
    
    def redis_ping(self):
        if self.redis.ping():
            print('Connected to Redis')
        return None

    def get_redis_value(self, key):
        if self.redis.exists(key):
            value = self.redis.get(key)
            return value
        return None

    def set_redis_value(self, key, value):
        response = self.redis.set(key, value)
        return response
