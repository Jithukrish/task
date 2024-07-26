# from django.urls import path
# from chat import consumers


# websocket_urlpatterns = [
#     path('chat/', consumers.ChatConsumer.as_asgi()),
# ]

from django.urls import re_path
from chat import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/messages/$', consumers.ChatConsumer.as_asgi()),
]