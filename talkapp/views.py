from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from .models import Post
from .forms import UserForm, UserUpdateForm, PostForm
from django.conf import settings
from django.contrib import messages
import time
import os

UPLOAD_DIR = settings.STATICFILES_DIRS[0] + '/images/'

def home(request):
    return render(request, 'talkapp/home.html')


def user_create(request):
    return render(request, 'talkapp/user_create.html')

def user_store(request):
    form = UserForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()

        profile = Profile()

        if 'file' in request.FILES:
            now = time.time()
            image_file = request.FILES['file']
            path = UPLOAD_DIR + str(now) + image_file.name
            destination = open(path, 'wb+')
            for chunk in image_file.chunks():
                destination.write(chunk)
            destination.close()
            profile.image = str(now) + image_file.name
        else:
            profile.image = "default.jpg"

        profile.user = user
        profile.save()

        user = authenticate(username=user.username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)

        return redirect('post_index')

    context = {
        "form": form,
    }
    return render(request, 'talkapp/user_create.html', context)

@login_required(login_url='/getlogin/')
def user_edit(request):
    user = request.user
    context = {
        'user' : user
    }
    return render(request, 'talkapp/user_edit.html', context)

@login_required(login_url='/getlogin/')
def user_update(request):
    form = UserUpdateForm(request.POST, instance=request.user)
    current_email = request.user.email
    if form.is_valid():
        user = form.save(commit=False)
        if form.cleaned_data['email'] != '':
            user.email = form.cleaned_data['email']
        else:
            user.email = current_email        
        if form.cleaned_data['password'] != '':
            password = form.cleaned_data['password']
            user.set_password(password)

        user.save()

        if 'file' in request.FILES:
            if user.profile.image != "default.jpg":
                old_image_file = UPLOAD_DIR + user.profile.image
                os.remove(old_image_file)

            now = time.time()
            image_file = request.FILES['file']
            path = UPLOAD_DIR + str(now) + image_file.name
            destination = open(path, 'wb+')
            for chunk in image_file.chunks():
                destination.write(chunk)
            destination.close()
            user.profile.image = str(now) + image_file.name
            user.profile.save()

        if form.cleaned_data['password'] != '':
            user = authenticate(username=user.username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)

        return redirect('post_index')

    context = {
        "form": form,
    }
    return render(request, 'talkapp/user_edit.html', context)


@login_required(login_url='/getlogin/')
def post_index(request):
    posts = Post.objects.all()
    context = {
        'posts' : posts
    }
    return render(request, 'talkapp/post_index.html', context)

@login_required(login_url='/getlogin/')
def post_create(request):
    return render(request, 'talkapp/post_create.html')

@login_required(login_url='/getlogin/')
def post_store(request):
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()

        return redirect('post_index')

    context = {
        "form": form,
    }
    return render(request, 'talkapp/post_create.html', context)

@login_required(login_url='/getlogin/')
def post_delete_all(request):
    Post.objects.all().delete()

    return redirect('post_index')


def getLogin(request):
    return render(request, 'talkapp/getlogin.html')

def postLogin(request):
    email = request.POST['email']
    password = request.POST['password']

    try:
       username = User.objects.get(email=email).username
    except User.DoesNotExist:
       username = None

    if username is not None:
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, 'You have successfully logged in')
                return redirect('post_index')

    messages.error(request, 'There was a problem with your email or password')
    return render(request, 'talkapp/getlogin.html')

def getLogout(request):
    logout(request)
    return render(request, 'talkapp/home.html')
