# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.hashers import make_password, check_password

from django.shortcuts import render, redirect
from datetime import datetime
from forms import SignUpForm,LoginForm
from models import User, SessionToken
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

def feed_view(request):
    return render(request,'feed.html')


def check_validation(request):
  if request.COOKIES.get('session_token'):
    session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
    if session:
      return session.user
  else:
    return None