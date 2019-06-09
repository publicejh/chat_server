import json
import requests
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.contrib.auth.models import AnonymousUser
from django.conf import settings


class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_str = request.META.get('HTTP_AUTHORIZATION')

        if not auth_str:
            raise exceptions.AuthenticationFailed('Authorization header is missing')

        token = auth_str.split(' ')[1]
        data_json = json.dumps({
            'token': token
        })
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        res = requests.post(settings.AUTH_SERVER_TOKEN_VALIDATION_URL, data=data_json,
                            headers=headers)

        if res.status_code != 200:
            print('auth fail: ', res.content)
            raise exceptions.AuthenticationFailed('Auth fail')

        return (AnonymousUser, None)
