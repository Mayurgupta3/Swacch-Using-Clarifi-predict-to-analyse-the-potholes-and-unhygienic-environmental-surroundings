# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime
from forms import SignUpForm, LoginForm, PostForm
from models import User, SessionToken, PostModel
from SwacchBharat.settings import BASE_DIR
from PIL import Image
from ClarifaiUsage import get_keywords_from_image
#from Sendgrid_usage import send_response
from imgurpython import ImgurClient
import sendgrid
from sendgrid.helpers.mail import *
from location import *



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
    elif request.method == "GET":
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

                print make_password(password), user.password
                if check_password(password, user.password):
                    token = SessionToken(user=user)
                    token.create_token()
                    token.save()
                    response = redirect('/feed/')
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
                main, sub = image.content_type.split('/')
                if not (main == 'image' and sub.lower() in ['jpeg', 'pjpeg', 'png', 'jpg']):
                    form = PostForm()

                    message = {'message': 'Enter JPEG or PNG image','form': form}
                    return render(request, 'post.html', message)

                else:
                    caption = form.cleaned_data.get('caption')
                    post = PostModel(user=user, image=image, caption=caption)
                    post.save()
                    path = str(BASE_DIR + '//' + post.image.url)


                    client = ImgurClient('31a3f32e7b361e8', '6ad2c7acd06b96d4d2e61ae015c2ea5ae016a059')
                    post_image_url = client.upload_from_path(path,anon=True)['link']

                    response_clarifai = get_keywords_from_image(post_image_url)
                    arr_of_dict = response_clarifai['outputs'][0]['data']['concepts']
                    print ("Mayur")
                    for i in range(0, len(arr_of_dict)):
                        keyword = arr_of_dict[i]['name']
                        print(keyword)
                        value = arr_of_dict[i]['value']
                        print(value)
                        print ("mayur")
                        if(keyword == 'Dirty' and value > 0.5):
                            is_dirty=True

                        elif (keyword == 'Clean'and value > 0.5):
                            is_dirty = False
                        else:
                            is_dirty =  False

                    post.is_dirty=is_dirty

                    post.save()
                    send_mail(post.image_url)

                    return redirect('/feed/')

        else:
            print request.body
            form = PostForm()
        return render(request, 'post.html', {'form' : form})
    else:
        return redirect('/login/')


def send_mail(post_image_url):
    print("qwerty")
    sg = sendgrid.SendGridAPIClient(apikey='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')

    from_email = Email("mgupta7042@gmail.com")
    to_email = Email("mgupta@gmail.com")
    message = "<html><body><h1>Image of the dirty area</h1><br><img src =" + post_image_url + "></body></html>"
    subject = "Image of dirty area!"
    content = Content("text/html", message)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)



def feed_view(request):
    user = check_validation(request)
    if user:
        posts = PostModel.objects.all().order_by('-created_on',)

        return render(request, 'feed.html', {'posts': posts})
    else:
        return redirect('/login/')




def logout_view(request):
    user = check_validation(request)
    if user is not None:
        latest_session = SessionToken.objects.filter(user=user).last()
        if latest_session:
            latest_session.delete()

    return redirect("/login/")


def check_validation(request):
  if request.COOKIES.get('session_token'):
    session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
    if session:
      return session.user
  else:
    return None
