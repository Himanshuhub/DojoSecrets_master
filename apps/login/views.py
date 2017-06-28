from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
from .models import Secret
from django.db.models import Count
import re
import bcrypt
password = "kittens"
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
    return render(request, 'login/index.html')

def register(request):
    if request.method == "POST":
        validation = User.objects.regVal(request.POST)

        if validation[0]:
            request.session['current_user']=validation[1].first_name
            request.session['user_id']=validation[1].id
            return redirect('/indexWall')
        else:
            for error in validation[1]:
                messages.error(request, error)
            return redirect('/')
    return redirect('/')

def login(request):
    if request.method == "POST":
        validation = User.objects.logVal(request.POST)

        if validation[0]:
            request.session['current_user']=validation[1].first_name
            request.session['user_id']=validation[1].id
            return redirect("indexWall")
        else:
            for error in validation[1]:
                messages.error(request, error)
            return redirect('/')
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

########################################################

def indexWall(request):
    if not "current_user" in request.session:
        messages.add_message(request, messages.INFO, "Must be logged in to view this page")
        return redirect('/')

    context = {
        "users": User.objects.all,
        "secrets": Secret.objects.annotate(num_likes=Count('like')).order_by('-created_at'),
        "current_user": User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'login/indexWall.html', context)

def add_secret(request):
    if request.method == "POST":
        new_post = Secret.objects.process_secret(request.POST, request.session['user_id'])
        print new_post.post
        return redirect('/indexWall')

def add_like(request):
    if request.method == "POST":
        user_likes = Secret.objects.process_like(request.POST)
        return redirect('indexWall')

def add_like2(request):
    if request.method == "POST":
        user_likes = Secret.objects.process_like(request.POST)
        return redirect('/most_popular')

def most_popular(request):
    if not "current_user" in request.session:
        messages.add_message(request, messages.INFO, "Must be logged in to view this page")
        return redirect('/')
    context = {
        "users": User.objects.all,
        "current_user": User.objects.get(id=request.session['user_id']),
        "secrets":Secret.objects.annotate(num_likes=Count('like')).order_by('-num_likes')
    }
    return render(request, 'login/most_popular.html', context)

def delete_secret(request):
    post_to_delete = Secret.objects.get(id=request.POST['secret_id'])
    post_to_delete.delete()
    return redirect('/indexWall')

def delete_secret2(request):
    post_to_delete = Secret.objects.get(id=request.POST['secret_id'])
    post_to_delete.delete()
    return redirect('/most_popular')

# def logoutWall(request):
#     request.session.clear()
#     return redirect('/')
