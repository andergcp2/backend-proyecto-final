from redis import Redis

ELASTICACHE_HOST = 'cluster-proyecto-final-ro.xpjxhf.ng.0001.use2.cache.amazonaws.com'
ELASTICACHE_PORT = 6379
redis = Redis(host=ELASTICACHE_HOST, port=ELASTICACHE_PORT, decode_responses=True, ssl=True)

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
        if self.redis.exists(key):
            response = self.redis.set(key, value)
            return response
        return None

