from django.urls import path, include
from . import views


urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('dashboard/', views.dashboard, name="dashboard"), 
    path('register/', views.Register.as_view(), name="register"),
    path('oauth/', include('social_django.urls')),
]
