from .common import *

config_secret_debug = json.loads(open(CONFIG_SECRET_DEBUG_FILE).read())

DEBUG = True
ALLOWED_HOSTS = config_secret_debug['django']['allowed_hosts']

# WSGI application
WSGI_APPLICATION = 'config.wsgi.debug.application'

ASGI_APPLICATION = 'config.routing.debug.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(config_secret_debug['django']['channel_layers_host'],
                       config_secret_debug['django']['channel_layers_port'])],
        },
    },
}

DATABASES = config_secret_debug['django']['databases']

CORS_ORIGIN_ALLOW_ALL = True

AUTH_SERVER_TOKEN_VALIDATION_URL = config_secret_debug['django']['auth_server_token_validation_url']
AUTH_SERVER_API_KEY = config_secret_debug['django']['auth_server_api_key']
AUTH_SERVER_GET_USER_API_URL = config_secret_debug['django']['auth_server_get_user_api_url']
