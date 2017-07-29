# -*- coding: utf-8 -*-
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
  password_mod = models.CharField(max_length=40)
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



