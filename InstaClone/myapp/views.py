# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from datetime import datetime
from forms import SignUpForm,LoginForm,PostForm
from models import User, SessionToken, PostModel
from InstaClone.settings import BASE_DIR

from imgurpython import ImgurClient
# Create your views here.

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User(name=name, password=make_password(password), email=email, username=username)
            user.save()
            return render(request, 'success.html')
    elif request.method=='GET':
        form = SignUpForm()
    return render(request, 'index.html', {'form': form})

def login_view(request):
    dict = {}
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = User.objects.filter(username=username).first()

            if user:
                # Check for the password
                print make_password(password), user.password
                if check_password(password, user.password):
                    token = SessionToken(user=user)
                    token.create_token()
                    token.save()
                    response = redirect('feed/')
                    response.set_cookie(key='session_token', value=token.session_token)
                    return response
                else:
                    dict['message'] = 'Incorrect Password! Please try again!'

    elif request.method == 'GET':
        form = LoginForm()

    dict['form'] = form
    return render(request,'login_view.html', dict)


def post_view(request):
    user = check_validation(request)
    if user:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                post = PostModel(user=user, image=image, caption=caption)
                post.save()

                path = str(BASE_DIR + '\\' + post.image.url)

                client = ImgurClient('31a3f32e7b361e8', '6ad2c7acd06b96d4d2e61ae015c2ea5ae016a059')
                post.image_url = client.upload_from_path(path,anon=True)['link']
                post.save()

                return redirect('/feed/')

        else:
            form = PostForm()
        return render(request, 'post.html', {'form' : form})
    else:
        return redirect('/login/')


def feed_view(request):
    user = check_validation(request)
    if user:

        posts = PostModel.objects.all().order_by('-created_on',)
        return render(request, 'feed.html', {'posts': posts})
    else:
        return redirect('/login/')


def check_validation(request):
  if request.COOKIES.get('session_token'):
    session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
    if session:
      return session.user
  else:
    return None