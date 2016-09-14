APP_SECRET = 'aslkjfas;lkj;asnw;qalkfjslXKNdsfV4ldihv2slkdfnl^ieurf['
AUTH_USERNAME = 'tuna'
AUTH_PASSWORD = 'beerme'

REDIS = {
    'host': 'localhost', 
    'port': 6379,
    'db': 0
}

THROTTLE = {
    'key': 'mock_app_throttle_window',
    'window': (1 * 60 * 60 * 1000),
    'limit': 200,
}

try:
    from local_settings import *
except ImportError:
    pass
