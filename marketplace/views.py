from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
#, (REDIRECT_FIELD_NAME, logout as auth_logout)
from django.contrib import messages
from .models import Post
import datetime
import calendar
import random
import re
import os

# Create your views here.

def login_user(request):
	return render(request, 'registration/login.html')

@login_required(login_url='login_user')
def logout_user(request):
	logout(request)
	return HttpResponseRedirect('/')

def authenticate_user(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is not None:
		login(request, user)
		request.session['user_id'] = user.id
		return HttpResponseRedirect(reverse('home'))
	else:
		return render(request, 'registration/login.html')

def new_user(request):
	return render(request, 'registration/new_user.html')

def create_user(request):
	if re.match(r'^[\w]+@umbc\.edu$', request.POST['email']):
		pass
	else:
		return render(request, 'registration/login.html')

	new_user = User.objects.create_user(first_name=request.POST['first'], username=request.POST['email'], email=request.POST['email'], password=request.POST['password'])
	new_user.last_name = request.POST['last']
	new_user.save()
	user = authenticate(username=request.POST['email'], password=request.POST['password'])
	login(request, user)
	return HttpResponseRedirect(reverse('home'))

@login_required(login_url='login_user')
def home(request):
	user = get_object_or_404(User, pk=request.session['user_id'])
	posts = Post.objects.all()
	context = {'user': user, 'posts': posts}
	return render(request, 'marketplace/home.html', context)

@login_required(login_url='login_user')
def profile(request):
	user = get_object_or_404(User, pk=request.session['user_id'])
	posts = Post.objects.filter(user=user)
	edit = request.GET.get('edit');
	context = {'user': user, 'posts': posts, 'edit': edit}
	return render(request, 'marketplace/profile.html', context)
	

@login_required(login_url='login_user')
def create_post(request):
	user = get_object_or_404(User, pk=request.session['user_id'])
	new_post = Post(user = user, subject = request.POST['subject'], description = request.POST['description'], cost = float(request.POST['cost']), creation_date = timezone.now())
	new_post.image = request.FILES['image']
	new_post.save()
	return HttpResponseRedirect(reverse('home'))

@login_required(login_url='login_user')
def view_post(request, post_id):
	post = get_object_or_404(Post, pk=post_id)
	seller = post.user
	context = {'post': post, 'seller': seller}
	return render(request, 'marketplace/view_post.html', context)

@login_required(login_url='login_user')
def update_post(request, post_id):
	post = get_object_or_404(Post, pk=post_id)
	post.subject = request.POST['subject']
	post.description = request.POST['description']
	post.cost = float(request.POST['cost'])
	post.save()
	return HttpResponseRedirect(reverse('view_post', args=(post.id, )))

@login_required(login_url='login_user')
def delete_post(request, post_id):
	post = get_object_or_404(Post, pk=post_id)
	post.delete()
	user = get_object_or_404(User, pk=request.session['user_id'])
	posts = Post.objects.filter(user=user)
	context = {'user': user, 'posts':posts}
	return render(request, 'marketplace/profile.html', context)

@login_required(login_url='login_user')
def checkout(request, post_id):
	post = get_object_or_404(Post, pk=post_id)
	context = {'post': post}
	return render(request, 'marketplace/checkout.html', context)

@login_required(login_url='login_user')
def buy(request, post_id):
	return render(request, 'marketplace/checkout.html')
