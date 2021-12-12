from django.urls import path
from . import views

app_name = "analyzer"
urlpatterns = [
    path('analyzer/', views.index, name="analyzer"),
    path('upload/', views.Analyze.as_view(), name="analyze"),
    path('chat/<int:pk>', views.Chat.as_view(), name="chat")
]
