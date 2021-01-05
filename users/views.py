from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.http import HttpResponse
import random

# Create your views here.

def register(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)    
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def forgotPswd(request):
    
    gifs = [
        "https://i.imgur.com/H5Y8QN5.gif",
        "https://i.giphy.com/media/yidUzqLoT6SxgKzv20/giphy.webp",
        "https://i.imgur.com/M1ftLXv.gif",
        "https://i.giphy.com/media/13jghlUIB6FHZm/giphy.webp"

    ]

    return render(request, 'vault/test.html', {'gif': gifs[random.randint(0, len(gifs)-1)]})