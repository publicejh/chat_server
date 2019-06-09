from django.urls import path

from .views import ChatListCreateView, ChatRetrieveUpdateDestroyView

app_name = 'chat'

urlpatterns = [
    path('', ChatListCreateView.as_view()),
    path('<pk>', ChatRetrieveUpdateDestroyView.as_view()),
]
