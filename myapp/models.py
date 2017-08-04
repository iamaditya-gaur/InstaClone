# -*- coding: utf-8 -*-
# TODO add comments to the code before final submission
from __future__ import unicode_literals

from django.db import models
import uuid

class SignUpModel(models.Model):
  '''
  this class is for user profile
  '''
  email_mod = models.EmailField(max_length=255)
  name_mod = models.CharField(max_length=120)
  username_mod = models.CharField(max_length=120)
  password_mod = models.CharField(max_length=255)
  created_on = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True)

class SessionToken(models.Model):
  '''
  this class is used to generate and store the session token
  '''
  user = models.ForeignKey(SignUpModel)
  session_token = models.CharField(max_length=255)
  created_on = models.DateTimeField(auto_now_add=True)
  is_valid = models.BooleanField(default=True)
  def create_token(self):
    # uuid.uuid4 generates a random alphanumeric string which is perfect for a session token.
    self.session_token = uuid.uuid4()

class PostModel(models.Model):
  user = models.ForeignKey(SignUpModel)
  image = models.FileField(upload_to='user_posts')
  image_url = models.CharField(max_length=255)
  caption = models.CharField(max_length=255)
  created_on = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True)
  has_liked = False

  @property
  def like_count(self):
    return len(LikeModel.objects.filter(post_id=self))

  @property
  def comment_cout(self):
    return CommentModel.objects.filter(post_id=self).order_by('created_on')

class LikeModel(models.Model):
  user = models.ForeignKey(SignUpModel)
  post_id = models.ForeignKey(PostModel)
  created_on = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True)

class CommentModel(models.Model):
  user = models.ForeignKey(SignUpModel)
  post_id = models.ForeignKey(PostModel)
  comment_text = models.CharField(max_length=555)
  created_on = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True)



