from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt

from .models import *

def signin(request):
    request.session['login'] = 'logout'
    return render(request, "signin.html")

def reg_process(request):
    if request.method == 'POST':
        errors = User.objects.register_validate(request.POST)

        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags = 'register')
            return redirect('/')
        else: 
            request.session['login'] = 'login'
            p = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(first_name = request.POST['first_name'],
            last_name = request.POST['last_name'], email = request.POST['email'],
            password = p)
            
            messages.success(request, "You have successfully registered!", extra_tags = 'register')

            request.session['id'] = user.id
            return redirect('/wall')

def log_process(request):
    if request.method == 'POST':
        errors = User.objects.login_validate(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags = 'login')
            return redirect('/')
        else:
            request.session['login'] = 'login'
            user = User.objects.filter(email = request.POST['email'])[0]
            request.session['id'] = user.id

            messages.success(request, "You are logged in!", extra_tags = 'login')

            return redirect('/wall')

def wall(request):
    if request.session['login'] == 'logout':
        return redirect('/')
    else: 
        user = User.objects.get(id = request.session['id'])
        everyone = User.objects.all()
        all_posts = Message.objects.all()
        all_comments = Comment.objects.all()
        context = {
            "u": user,
            "users": everyone,
            "posts": all_posts,
            "replies": all_comments
        }
        return render(request, "wall.html", context)

def clear(request):
    User.objects.all().delete()
    return redirect('/')

def wall_post(request):
    if request.method == 'POST':
        errors = User.objects.post_validate(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags = 'message')
            return redirect('/wall')
        else:
            poster = User.objects.get(id = request.session['id'])
            Message.objects.create(message = request.POST['message'], user = poster)
            return redirect('/wall')

def wall_comment(request, num):
    if request.method == 'POST':
        errors = User.objects.comment_validate(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags = 'comment')
            return redirect('/wall')
        else:
            post = Message.objects.get(id = num)
            poster = User.objects.get(id = request.session['id'])
            Comment.objects.create(comment = request.POST['comment'], user = poster, message = post)
            return redirect('/wall')

def wall_delete(request, num):
    post = Message.objects.get(id = num)
    post.delete()
    return redirect('/wall')

def clear_all(request):
    Message.objects.all().delete()
    return redirect('/wall')

'''
20cooler@eq.com
Dashie20

partypony@eq.com
Pinkie10

generosity@eq.com
Gem12345
'''