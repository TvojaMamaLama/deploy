from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic import CreateView
from .forms import UserForm
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from .models import Room, Chat, User
from rest_framework.response import Response


class MainPageView(TemplateView):
    template_name = 'index.html'


class RegistrationView(CreateView):
    template_name = 'registration/register.html'

    def get_context_data(self, **kwargs):
        form = UserForm()
        context = {'form': form}
        return context

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            passwd = form.cleaned_data['password1']
            user = authenticate(username=username, password=passwd)
            login(request, user)
            return redirect('index')
        return render(request, 'registration/register.html', context={'form': form, 'error': 'Username exist'})


def FindUser(request):
    try:
        user = User.objects.get(username=request.POST['username'])
    except User.DoesNotExist:
        user = 1
    if user == request.user:
        return render(request, 'index.html', context={'user1': []})
    return render(request, 'index.html', context={'user1': user})


class chat(APIView):
    def post(self, request):
        user = User.objects.get(username=request.data['username'])
        Chat.objects.create(room_id=request.data['room'], text=request.data['text'], user=user)
        return Response()


def room(request, joiner):
    try:
        user = User.objects.get(username=joiner)
    except:
        return redirect('index')

    try:
        room = Room.objects.get(creator=request.user, joiner=user)
    except:
        try:
            room = Room.objects.get(creator=user, joiner=request.user)
        except:
            room = Room.objects.create(creator=request.user, joiner=user)
    history = Chat.objects.filter(room=room)[:30]
    return render(request, 'room.html', {'room_name': room.id, 'history': history})

