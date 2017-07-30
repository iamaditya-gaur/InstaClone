# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from forms import SignUpForm,LoginForm
from models import SignUpModel, SessionToken
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password

def signup_view(request):
    if request.method == "GET":
        form = SignUpForm()
    elif request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username_mod']
            name = form.cleaned_data['name_mod']
            email = form.cleaned_data['email_mod']
            password = form.cleaned_data['password_mod']
            # saving the above extracted data to db
            user = SignUpModel(username_mod=username , name_mod = name , email_mod=email , password_mod=make_password(password))
            user.save()
            return render(request, 'success.html')
    return render(request, 'index.html', {'form': form})

def login_view(request):
    if request.method == 'GET':
        form = LoginForm()
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            usrname = form.cleaned_data.get('username_mod')
            passw = form.cleaned_data.get('password_mod')
            # Checking if the username is present in the database
            user_login = SignUpModel.objects.filter(username_mod=usrname).first()
            if user_login:
                # Checking for the password for that username
                if check_password(passw, user_login.password_mod):
                    # Create and store a session token for this user
                    sess = SessionToken(user=user_login)
                    sess.create_token()
                    sess.save()
                    response = redirect ('myapp/feed/')
                    response.set_cookie(key="session_token", value="sess.session_token")
                    return response
        else:
            return render(request , 'error.html')
    return render(request, 'login.html', {'loginform': form})


