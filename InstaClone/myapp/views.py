# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from datetime import datetime
from forms import SignUpForm,LoginForm,PostForm,LikeForm,CommentForm
from models import User, SessionToken, PostModel, LikeModel, CommentModel
from InstaClone.settings import BASE_DIR
from PIL import Image
from ClarifaiUsage import get_keywords_from_image
from Sendgrid_usage import send_response


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
                main, sub = image.content_type.split('/')
                if not (main == 'image' and sub.lower() in ['jpeg', 'pjpeg', 'png', 'jpg']):
                    form = PostForm()
                    message = {'message': 'Enter JPEG or PNG image','form': form}
                    return render(request, 'post.html', message)

                else:

                    caption = form.cleaned_data.get('caption')
                    post = PostModel(user=user, image=image, caption=caption)
                    post.save()
                    path = str(BASE_DIR + '\\' + post.image.url)

                    client = ImgurClient('31a3f32e7b361e8', '6ad2c7acd06b96d4d2e61ae015c2ea5ae016a059')
                    post.image_url = client.upload_from_path(path,anon=True)['link']
                    response_clarifai = get_keywords_from_image(post.image_url)
                    arr_of_dict = response_clarifai['outputs'][0]['data']['concepts']
                    for i in range(0, len(arr_of_dict)):
                        keyword = arr_of_dict[i]['name']
                        value = arr_of_dict[i]['value']
                        if(keyword == 'Dirty' and value >0.5):
                            is_dirty=True
                            message_payload = {
                                "personalizations": [
                                    {
                                        "to": [
                                            {
                                                "email": 'mgupta7042@gmail.com' #authority
                                            }
                                        ],
                                        "subject": 'Dirty area!'
                                    }
                                ],
                                "from": {
                                    "email": "uditk53@gmail.com",
                                    "name": 'Swacch Bharat'
                                },
                                "content": [
                                    {
                                        "type": "text/html",
                                        "value": "<h1>Swacch Bharat</h1><br><br>  <img src =" + post.image_url + " <br>"

                                    }
                                ]
                            }

                            send_response(message_payload)

                        elif (keyword == 'Clean'and value >0.5):
                            is_dirty = False
                        else:
                            is_dirty =  False

                    post.is_dirty=is_dirty

                    post.save()

                    return redirect('/feed/')

        else:
            print request.body
            form = PostForm()
        return render(request, 'post.html', {'form' : form})
    else:
        return redirect('/login/')

def feed_view(request):
    user = check_validation(request)
    if user:
        posts = PostModel.objects.all().order_by('-created_on',)
        for post in posts:
            existing_like = LikeModel.objects.filter(post_id=post.id, user=user).first()
            if existing_like:
                post.has_liked = True
        return render(request, 'feed.html', {'posts': posts})
    else:
        return redirect('/login/')

def like_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            existing_like = LikeModel.objects.filter(post_id=post_id, user=user).first()
            if not existing_like:
                LikeModel.objects.create(post_id=post_id, user=user)
            else:
                existing_like.delete()
            return redirect('/feed/')
    else:
        return redirect('/login/')

def comment_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id
            comment_text = form.cleaned_data.get('comment_text')
            comment = CommentModel.objects.create(user=user, post_id=post_id, comment_text=comment_text)
            post = PostModel.objects.filter(id=post_id).first()
            comment.save()
            comment_email(user.username, post.user.email)
            return redirect('/feed/')
        else:
            return redirect('/feed/')
    else:
        return redirect('/login')


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

def comment_email(commentor, to_email):
    msg_payload = {
        "personalizations": [
            {
                "to": [
                    {
                        "email": to_email
                    }
                ],
                "subject": 'Someone reacted to your post!'
            }
        ],
        "from": {
            "email": "uditk53@gmail.com",
            "name": 'Swacch Bharat'
        },
        "content": [
            {
                "type": "text/html",
                "value": '<h1>Swacch Bharat</h1><br><br> ' +commentor+' just commented on your post. <br>'

            }
        ]
    }
    send_response(msg_payload)