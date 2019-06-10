from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from chats.models import Chat, Message
from chats.views import get_user_contact, get_current_chat, get_user_detail
from .serializers import ChatSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import status
from rest_framework_api_key.permissions import HasAPIKey

channel_layer = get_channel_layer()


class ChatListCreateView(ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def get_queryset(self):
        queryset = Chat.objects.all()
        user_id = self.request.query_params.get('userId', None)
        sig_id = self.request.query_params.get('sigId', None)
        if user_id is not None and sig_id is not None:
            contact = get_user_contact(user_id)
            queryset = contact.chats.filter(sig_id=sig_id)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ChatSerializer(queryset, many=True)
        return Response(serializer.data)


class ChatRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


class ChatSendFileView(APIView):
    authentication_classes = []
    permission_classes = (HasAPIKey, )

    def post(self, request):
        user_id = request.data['from']
        is_file = request.data['is_file']
        file_path = request.data['file_path']
        chat_id = request.data['chat_id']

        message = Message.objects.create(
            contact=get_user_contact(user_id),
            is_file=is_file,
            file_path=file_path
        )

        target_chat = get_current_chat(chat_id)
        target_chat.messages.add(message)
        target_chat.save()

        content = {
            'command': 'new_message',
            'message': {
                'id': message.id,
                'author': message.contact.user_id,
                'content': message.content,
                'is_file': message.is_file,
                'file_path': message.file_path,
                'timestamp': str(message.timestamp),
                'author_name': get_user_detail(message.contact.user_id)['username']
            }
        }

        try:
            async_to_sync(channel_layer.group_send)(
                target_chat.group_name(),
                {
                    "type": "chat_message",  # call chat_message method
                    "message": content,
                }
            )
            return Response({'result': 8200}, status=status.HTTP_200_OK)
        except Exception as ex:
            print(ex)
            return Response({'result': 8400}, status=status.HTTP_200_OK)
