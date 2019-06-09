from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from chats.models import Chat
from chats.views import get_user_contact
from .serializers import ChatSerializer
from rest_framework.response import Response


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
