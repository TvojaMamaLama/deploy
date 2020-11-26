from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Room, Chat
from rest_framework.response import Response


class MainPageView(TemplateView):
    template_name = 'index.html'


class RegistrationView(CreateView):
    template_name = 'registration/register.html'

    def get_context_data(self, **kwargs):
        form = UserCreationForm()
        context = {'form': form}
        return context

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            passwd = form.cleaned_data['password1']
            user = authenticate(username=username, password=passwd)
            login(request, user)
            return redirect('index')
        return render(request, 'registration/register.html', context={'form': form, 'error': 'Username exist'})


def FindUser(request):
    users = User.objects.filter(username__contains=request.POST['username']).exclude(username=request.user.username)
    return render(request, 'index.html', context={'users': users})


class chat(APIView):
    def post(self, request):
        user = User.objects.get(username=request.data['username'])
        Chat.objects.create(room_id=request.data['room'], text=request.data['text'], user=user)
        return Response()


def room(request, joiner):
    try:
        user = User.objects.get(username=joiner)
    except User.DoesNotExist:
        return render()
    try:
        room = Room.objects.filter(users__in=[request.user, user])[0]
    except Room.DoesNotExist:
        room = Room.objects.create()
        room.users.add(request.user)
        room.users.add(user)
        room.save()
    history = Chat.objects.filter(room=room)[:100]
    return render(request, 'room.html', {'room_name': room.id, 'history': history})

