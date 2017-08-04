# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from forms import SignUpForm,LoginForm, PostForm, LikeForm, CommentForm
from models import SignUpModel, SessionToken, PostModel, LikeModel, CommentModel
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from imgurpython import ImgurClient
from my_web_project.settings import BASE_DIR
from datetime import timedelta
from django.utils import timezone
from clarifai.rest import ClarifaiApp
app_clarifai = ClarifaiApp(api_key='d395bb2c633d44be89091081ee37f752')

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

#TODO change redirect from post to feed page in line 45
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
                    response = redirect ('/myapp/feed/')
                    response.set_cookie(key='session_token', value=sess.session_token)
                    return response
        else:
            return render(request , 'error.html')
    return render(request, 'login.html', {'loginform': form})

def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
        if session:
            time_to_live = session.created_on + timedelta(days=1)
            if time_to_live > timezone.now():
                return session.user
            else:
                redirect('myapp/login/')
        else:
            return None

def feed_view(request):
    user_valid = check_validation(request)
    if user_valid:
        post_images = PostModel.objects.all().order_by('-created_on')

        for post in post_images:
            existing_like = LikeModel.objects.filter(user=user_valid, post_id=post.id).first()
            if existing_like:
                post.has_liked = True
            else:
                post.has_liked = False

        return render(request, 'feeds.html', {'posts_form':post_images})
    else:
        return redirect('/myapp/login')

def like_view(request):
    user_valid = check_validation(request)
    if user_valid and request.method == "POST":
        lform = LikeForm(request.POST)
        if lform.is_valid():
            postid = lform.cleaned_data.get("post").id
            existing_like = LikeModel.objects.filter(post_id=postid, user=user_valid).first()
            if not existing_like:
                LikeModel.objects.create(post_id= postid, user= user_valid)
            else:
                existing_like.delete()
            return redirect('myapp/feed')
    else:
        return redirect('/myapp/login')

def comment_view(request):
    user_valid = check_validation(request)
    if user_valid and request.method == "POST":
        cform = CommentForm(request.POST)
        if cform.is_valid():
            postid = cform.cleaned_data.get("post_id").id
            comment_txt = cform.cleaned_data.get("coment_text")
            comment = CommentModel.objects.create(user=user_valid, post_id=postid, comment_text=comment_txt)
            comment.save()
            return redirect("myapp/feed")
    else:
        return redirect('/myapp/login')

# Method to check wether the post if NSFW or SFW
def nsfw(img_url):
    model = app_clarifai.models.get('nsfw-v1.0')
    response = model.predict_by_url(url=img_url)
    i = len(response["outputs"])
    i -= 1
    val_sfw = response["outputs"][i]["data"]["concepts"][0]["value"]
    val_nsfw = response["outputs"][i]["data"]["concepts"][1]["value"]
    if val_nsfw > val_sfw:
        return None
    else:
        return (1)

#TODO deal with imgur file extension error
def post_view(request):
    user_valid = check_validation(request)
    if user_valid:
        if request.method == "GET":
            pform = PostForm()
        elif request.method == "POST":
            pform = PostForm(request.POST, request.FILES)
            if pform.is_valid():
                image_data = pform.cleaned_data.get('image')
                caption_data = pform.cleaned_data.get('caption')
                post_data = PostModel(user=user_valid, image=image_data, caption=caption_data)
                post_data.save()
                client = ImgurClient('42f5481cbd0457f', '7bdf7000862e4cc52c8c320aa8fbb7437216c072')
                path = BASE_DIR + "/" + post_data.image.url
                image_url = client.upload_from_path(path, anon=True)['link']
                caption = post_data.caption
                type_nsfw = nsfw(image_url)
                if type_nsfw is 1:
                    post_data.image_url = image_url
                    post_data.save()
                else:
                     PostModel.objects.latest('created_on').delete()

                return redirect('/myapp/feed')
        return render(request, 'post.html', {'formdata': pform})
    else:
        return redirect('/myapp/login')



