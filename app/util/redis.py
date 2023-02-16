import redis
jwt_redis_blocklist = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=True
)

def is_redis_available(r):
    try:
        r.ping()
        print("Successfully connected to redis")
    except (redis.exceptions.ConnectionError, ConnectionRefusedError):
        print("Redis connection error!")
        return False
    return True

if is_redis_available(jwt_redis_blocklist):
    print("Yay!")