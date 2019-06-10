from django.urls import path

from .views import ChatListCreateView, ChatRetrieveUpdateDestroyView, ChatSendFileView

app_name = 'chats'

urlpatterns = [
    path('', ChatListCreateView.as_view()),
    path('<int:pk>', ChatRetrieveUpdateDestroyView.as_view()),
    path('images', ChatSendFileView.as_view()),
]
