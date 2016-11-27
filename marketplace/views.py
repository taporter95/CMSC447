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
from django.core.exceptions import *
#, (REDIRECT_FIELD_NAME, logout as auth_logout)
from django.contrib import messages
from .models import Post
from .models import UserModel
import datetime
import calendar
import random
import re
import os

# Create your views here.
@login_required(login_url='login_user')
def redirect(request):
	return HttpResponseRedirect('/')

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

#TODO The page doesnt fit the screen now with the extra umbcid field need to make it bigger or scrollable
def new_user(request):
	return render(request, 'registration/new_user.html')

def create_user(request):
	if re.match(r'^[\w]+@umbc\.edu$', request.POST['email']):
		pass
	else:
		messages.add_message(request, messages.ERROR, 'You must have a valid UMBC email')
		return HttpResponseRedirect(reverse('new_user'))
	
	if re.match('[A-Z][A-Z][0-9][0-9][0-9][0-9][0-9]', request.POST['umbcid'].upper()):
		pass
	else:
		messages.add_message(request, messages.ERROR, 'You must have a valid UMBC Id')
		return HttpResponseRedirect(reverse('new_user'))
		

	if request.POST['password'] != request.POST['repassword']:
		messages.add_message(request, messages.ERROR, 'Passwords do not match')
		return HttpResponseRedirect(reverse('new_user'))

	try: 
		User.objects.get(username=request.POST['email'])
	except ObjectDoesNotExist:
		new_user = User.objects.create_user(first_name=request.POST['first'], username=request.POST['email'], email=request.POST['email'], password=request.POST['password'])
		new_user.last_name = request.POST['last']	
		new_user.save()
		really_new_user = UserModel(user=new_user, umbcid=request.POST['umbcid'], rating=5)
		really_new_user.save()

		user = authenticate(username=request.POST['email'], password=request.POST['password'])
		login(request, user)
		request.session['user_id'] = user.id
		return HttpResponseRedirect(reverse('home'))
	messages.add_message(request, messages.ERROR, 'User is already registered for this email')
	return HttpResponseRedirect(reverse('new_user'))

@login_required(login_url='login_user')
def home(request):
	user = get_object_or_404(User, pk=request.session['user_id'])
	try:
		userstuff = UserModel.objects.get(user=user)
	except:
		return HttpResonse("<html>Shouldnt hit here database needs to be redone.</html>")
	try:
		limit = float(request.POST['limit'])
	except:
		limit = float(100000000)

	try:
		if request.POST['free']:
			try:
				posts = Post.objects.filter(subject__contains=request.POST['keyword'], cost=0)
			except:
				posts = Post.objects.all().filter(cost=0)
	except:
		try:
			posts = Post.objects.filter(subject__contains=request.POST['keyword'], cost__lte=limit)
		except:
			posts = Post.objects.all().filter(cost__lte=limit)

	post_paginator = Paginator(posts, 5)

	page = request.GET.get('page')

	try:
		post_page = post_paginator.page(page)
	except PageNotAnInteger:
		post_page = post_paginator.page(1)
	except EmptyPage:
		post_page = post_paginator.page(post_paginator.num_pages)

	context = {'user': user, 'post_page': post_page, 'posts': posts,}
	return render(request, 'marketplace/home.html', context)

@login_required(login_url='login_user')
def search_results(request):
	
	try:
		limit = float(request.POST['limit'])
	except:
		limit = float(100000000)

	try:
		if request.POST['free']:
			try:
				posts = Post.objects.filter(subject__contains=request.POST['keyword'], cost=0)
			except:
				posts = Post.objects.all().filter(cost=0)
	except:
		try:
			posts = Post.objects.filter(subject__contains=request.POST['keyword'], cost__lte=limit)
		except:
			posts = Post.objects.all().filter(cost__lte=limit)

 
	post_paginator = Paginator(posts, 5)

	page = request.GET.get('page')

	try:
		post_page = post_paginator.page(page)
	except PageNotAnInteger:
		post_page = post_paginator.page(1)
	except EmptyPage:
		post_page = post_paginator.page(post_paginator.num_pages)

	context = {'post_page': post_page, 'posts': posts}
	return render(request, 'marketplace/search_results.html', context)

@login_required(login_url='login_user')
def profile(request):
	user = get_object_or_404(User, pk=request.session['user_id'])
	try:
		userstuff = UserModel.objects.get(user=user)
	except:
		return HttpResonse("<html>Shouldnt hit here database needs to be redone.</html>")
	
	posts = Post.objects.filter(user=user)
	
	post_paginator = Paginator(posts, 5)
	page = request.GET.get('page')
	
	try:
		post_page = post_paginator.page(page)
	except PageNotAnInteger:
		post_page = post_paginator.page(1)
	except EmptyPage:
		post_page = post_paginator.page(post_paginator.num_pages)
	
<<<<<<< HEAD
	edit = request.GET.get('edit');
	ratingcounter = range(0,userstuff.rating)
	missing = range(0, 5 - userstuff.rating)
	context = {'user': user, 'post_page': post_page, 'posts': posts, 'edit': edit, 'ratingcounter': ratingcounter, 'missing': missing}
=======
	edit = request.GET.get('edit')
	context = {'user': user, 'post_page': post_page, 'posts': posts}
>>>>>>> bf659bb736a3a59a4070fba4d663a6617d82b4e2
	return render(request, 'marketplace/profile.html', context)

@login_required(login_url='login_user')
def update_profile(request):
	user = get_object_or_404(User, pk=request.session['user_id'])
	user.first_name = request.POST.get('first')
	user.last_name = request.POST.get('last')
	user.email = request.POST.get('email')

	user.save()
	return HttpResponseRedirect(reverse('profile'))

@login_required(login_url='login_user')
def create_post(request):
	flag = 0;
	user = get_object_or_404(User, pk=request.session['user_id'])
	new_post = Post(user = user, description = request.POST['description'], post_type = request.POST['type'], creation_date = timezone.now())
	
	if len(request.POST['subject']) == 0:
		flag = 1;
		messages.add_message(request, messages.ERROR, 'Post Failed: Subject is a required field')
	else:
		new_post.subject = request.POST['subject']

	try:
		new_post.cost = float(request.POST['cost'])
	except:
		flag = 1;
		messages.add_message(request, messages.ERROR, 'Post Failed: Invalid price entry')

	if flag:
		HttpResponseRedirect(reverse('home'))

	try:
		new_post.image = request.FILES['image']
	except:
		pass

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




