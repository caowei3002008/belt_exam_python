# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from forms import *
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)
from django.contrib import messages
from models import *


def form_display():
    registerForm = UserRegis()
    loginForm = login_form()
    context = {
        'registerForm': registerForm,
        'loginForm': loginForm
    }
    return context

def index(request):
    registerForm = UserRegis()
    loginForm = login_form()
    if request.method == 'POST':
        if UserRegis(request.POST):
            registerForm = UserRegis(request.POST)
            if registerForm.is_valid():
                user = registerForm.save(commit=False)
                clearPassNoHash = registerForm.cleaned_data['password']
                user.set_password(clearPassNoHash)
                user.save()
                context = {
                    'registerForm' : UserRegis,
                    'loginForm' : loginForm
                }
                messages.success(request, 'You have successfully registered.')
                return render(request, 'friends/index.html',  context)
    context = {
        'registerForm': registerForm,
        'loginForm': loginForm
    }
    return render(request, 'friends/index.html', context)


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email_login']
        password = request.POST['password_login']
        all_user = User.objects.all()
        email_store = []
        for single_user in all_user:
            email_store.append(single_user.email)
        print email_store
        if email in email_store:
            u = User.objects.get(email = email)
            encrypted = u.password
            if check_password(password, encrypted):
                print('success')
                request.session['login'] = True
                request.session['id'] = u.id
                login_user = User.objects.get(id=request.session['id'])
                your_friend = friend_display(request.session['id'])
                other_user = other_user_display(request.session['id'])

                context = {
                    'login_user': login_user,
                    'friend': your_friend,
                    'other_user': other_user
                }
                print login_user.alias
                return render(request, 'friends/login.html', context)
            else:
                messages.error(request, 'Wrong password')
        else:
            messages.error(request, 'Wrong email')
    return render(request, 'friends/index.html', form_display())


def logout_form(request):
    request.session['login'] = False
    request.session['id'] = 0
    return redirect('http://127.0.0.1:8000/main')


def home(request):
    login_user = User.objects.get(id=request.session['id'])
    your_friend = friend_display(request.session['id'])
    other_user = other_user_display(request.session['id'])

    context = {
        'login_user': login_user,
        'friend': your_friend,
        'other_user': other_user
    }
    return render(request, 'friends/login.html', context)


def addFriend(user_id, friend_id):

    Friends.objects.create(user_friend_id=user_id, second_friend_id=friend_id)
    Friends.objects.create(user_friend_id=friend_id, second_friend_id=user_id)


def removeFriend(user_id, friend_id):
    friendship1 = Friends.objects.get(user_friend_id=user_id, second_friend_id=friend_id)
    friendship2 = Friends.objects.get(user_friend_id=friend_id, second_friend_id=user_id)
    friendship1.delete()
    friendship2.delete()


def friend_display(user_id):
    store = []
    if Friends.objects.filter(user_friend_id=user_id):
        friends = Friends.objects.filter(user_friend_id=user_id)
        for friend in friends:
            b = User.objects.get(id = friend.second_friend_id)
            store.append(b)
        return store
    else:
        store = None
        return store

def other_user_display(user_id):
    friend_id_store = []
    friend_store = []
    not_friend_store = []
    if Friends.objects.filter(user_friend_id = user_id):
        friend_id_store.append(user_id)
        b = Friends.objects.filter(user_friend_id = user_id)
        for bb in b:
            friend_id_store.append(bb.second_friend_id)
        for friend in friend_id_store:
            b = User.objects.get(id = friend)
            friend_store.append(b)
        all_user = User.objects.all()
        for user in all_user:
            if user not in friend_store:
                not_friend_store.append(user)
        return not_friend_store

    else:
        others = User.objects.exclude(id = user_id)
        return others


def add(request):
    friend_id = request.POST['friend_id']
    addFriend(request.session['id'], friend_id)

    login_user = User.objects.get(id=request.session['id'])
    your_friend = friend_display(request.session['id'])
    other_user = other_user_display(request.session['id'])

    context = {
        'login_user': login_user,
        'friend': your_friend,
        'other_user': other_user
    }
    return render(request, 'friends/login.html', context)


def remove(request):
    remove_friend_id = request.POST['remove_friend_id']
    removeFriend(request.session['id'], remove_friend_id)

    login_user = User.objects.get(id=request.session['id'])
    your_friend = friend_display(request.session['id'])
    other_user = other_user_display(request.session['id'])

    context = {
        'login_user': login_user,
        'friend': your_friend,
        'other_user': other_user
    }
    return render(request, 'friends/login.html', context)


def show(request):
    user_info = User.objects.get(id = request.POST['show_id'])
    return render(request, 'friends/profile.html', {'user':user_info})







