# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from forms import SignUpForm,LoginForm
from models import SignUpModel, SessionToken
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password

def signup_view(request):
    if request.method == "GET":
        form = SignUpForm()
    elif request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # saving the above extracted data to db
            user = SignUpModel(username_mod=username , name_mod = name , email_mod=email , password_mod=make_password(password))
            user.save()
            return render(request, 'success.html')
    return render(request, 'index.html', {'form': form})

def login_view(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'loginform':form})
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            usrname = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # Checking if the username is present in the database
            user_login = SignUpModel.objects.filter(username_mod=usrname).first()
            if user_login:
                # Checking for the password for that username
                if check_password(password, user_login.password):
                    token = SessionToken(user=user_login)
                    token.create_token()
                    token.save()





