from rest_framework import serializers
from chats.models import Chat
from chats.views import get_user_contact


class ContactSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value


class ChatSerializer(serializers.ModelSerializer):
    participants = ContactSerializer(many=True)

    class Meta:
        model = Chat
        fields = ('id', 'messages', 'participants', 'sig_id', 'name', )
        read_only = ('id',)

    def create(self, validated_data):
        participants = validated_data.pop('participants')
        sig_id = validated_data.pop('sig_id')
        chat_name = validated_data.pop('name')
        chat = Chat(sig_id=sig_id, name=chat_name)
        chat.save()
        for user_id in participants:
            contact = get_user_contact(user_id)
            chat.participants.add(contact)
        chat.save()
        return chat
