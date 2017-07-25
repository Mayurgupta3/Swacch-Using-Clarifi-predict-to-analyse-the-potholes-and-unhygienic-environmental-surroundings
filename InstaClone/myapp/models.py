# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django\
    .db import models
import uuid
class User(models.Model):
    username = models.CharField(max_length=120,default='')
    name = models.CharField(max_length=120,default='')
    email = models.EmailField(default='')
    password = models.CharField(max_length=40,default='')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

class SessionToken(models.Model):
	user = models.ForeignKey(User)
	session_token = models.CharField(max_length=255)
	last_request_on = models.DateTimeField(auto_now=True)
	created_on = models.DateTimeField(auto_now_add=True)
	is_valid = models.BooleanField(default=True)

	def create_token(self):
		self.session_token = uuid.uuid4()

class PostModel(models.Model):
	user = models.ForeignKey(User)
	image = models.FileField(upload_to='user_images')
	image_url = models.CharField(max_length=255)
	caption = models.CharField(max_length=240)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)
	has_liked = False