from django.urls import path

from .views import MainPageView, RegistrationView, FindUser, room, chat


urlpatterns = [
    path('', MainPageView.as_view(), name='index'),
    path('search/', FindUser, name='search'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('chat', chat.as_view()),
    path('chat/<str:joiner>/', room, name='room')
]