from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Aggregate
from django.shortcuts import render, redirect

from paper.models import PaperItem


def login_user(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        return render(request, 'profiles/login.html', {'error': 'Login failed.'})
    return render(request, 'profiles/login.html', {})


def register_user(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        password_2 = data.get('password_2')
        user = User.objects.filter(username=username)

        if not user.exists() and username is not '' and password is not '' and password_2 is not '':
            if password == password_2:
                new_user = User.objects.create_user(username=username, password=password)
                new_user.save()

                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('/')
                return render(request, 'profiles/register.html', {'error': 'Login failed.'})
            return render(request, 'profiles/register.html', {'error': 'Passwords do not match.'})
        return render(request, 'profiles/register.html', {'error': 'Username is taken.'})
    return render(request, 'profiles/register.html', {})


@login_required()
def account(request):
    papers = PaperItem.objects.filter(owner=request.user).order_by('-created')
    return render(request, 'profiles/index.html', {'papers': papers})


@login_required()
def view_mentions(request):
    data = request.GET
    slug = data.get('paper')
    paper = PaperItem.objects.filter(slug=slug)

    if paper.exists():
        mentions = PaperItem.objects.filter(body__contains='@' + slug)
        return render(request, 'profiles/view_mentions.html', {'paper': paper.first(), 'mentions': mentions})

    return render(request, 'profiles/view_mentions.html', {})
