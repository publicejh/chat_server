from .common import *

config_secret_deploy = json.loads(open(CONFIG_SECRET_DEPLOY_FILE).read())

DEBUG = False
ALLOWED_HOSTS = config_secret_deploy['django']['allowed_hosts']

# WSGI application
WSGI_APPLICATION = 'config.wsgi.deploy.application'

ASGI_APPLICATION = 'config.routing.deploy.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(config_secret_deploy['django']['channel_layers_host'],
                       config_secret_deploy['django']['channel_layers_port'])],
        },
    },
}

DATABASES = config_secret_deploy['django']['databases']

CORS_ORIGIN_WHITELIST = [
]

AUTH_SERVER_TOKEN_VALIDATION_URL = config_secret_deploy['django']['auth_server_token_validation_url']
AUTH_SERVER_API_KEY = config_secret_deploy['django']['auth_server_api_key']
AUTH_SERVER_GET_USER_API_URL = config_secret_deploy['django']['auth_server_get_user_api_url']
