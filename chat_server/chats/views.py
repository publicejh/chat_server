from django.shortcuts import get_object_or_404
from .models import Chat, Contact
import requests
import json
from django.conf import settings


def get_last_20_messages(chat_id, end_at=None):
    chat = get_object_or_404(Chat, id=chat_id)
    if end_at:
        return chat.messages.filter(id__lt=end_at).order_by('-timestamp').all()[:20]
    else:
        return chat.messages.order_by('-timestamp').all()[:20]


def get_user_contact(user_id):
    try:
        return Contact.objects.get(user_id=user_id)
    except Contact.DoesNotExist:
        user_detail = get_user_detail(user_id)
        return Contact.objects.create(user_id=user_id, username=user_detail['username'])


def get_current_chat(chat_id):
    return get_object_or_404(Chat, id=chat_id)


def get_user_detail(pk):
    headers = {
        'Content-Type': 'application/json', 'Accept': 'application/json',
        'Authorization': 'Api-Key ' + settings.AUTH_SERVER_API_KEY
    }
    res = requests.get(settings.AUTH_SERVER_GET_USER_API_URL + '/' + str(pk), headers=headers)

    if res.status_code != 200:
        return None
    print('aaaaa', res.content)
    return json.loads(res.content)
