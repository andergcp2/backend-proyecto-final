from redis import Redis

ELASTICACHE_HOST = 'cluster-proyecto-final-ro.xpjxhf.ng.0001.use2.cache.amazonaws.com'
ELASTICACHE_PORT = 6379
redis = Redis(host=ELASTICACHE_HOST, port=ELASTICACHE_PORT, decode_responses=True, ssl=True)

def redis_ping():
    if redis.ping():
        print('Connected to Redis')
    return None

def get_redis_value(key):
    if redis.exists(key):
        value = redis.get(key)
        return value
    return None

def set_redis_value(key, value):
    response = redis.set(key, value)
    return response

