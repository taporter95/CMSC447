from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
# , (REDIRECT_FIELD_NAME, logout as auth_logout)
from django.contrib import messages
from .models import Post, Transaction, UserModel
import datetime
import calendar
import random
import re


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
        # Don't let user log in if they're banned
        userstuff = UserModel.objects.get(user=user)
        if userstuff is None:
            return render(request, 'registration/login.html')
        elif userstuff.banned:
            messages.add_message(request, messages.ERROR, 'You have been banned from this site.')
            return render(request, 'registration/login.html')
        else:
            login(request, user)
            request.session['user_id'] = user.id
            return HttpResponseRedirect(reverse('home'))
    else:
        messages.add_message(request, messages.ERROR, 'Invalid username or password')
        return render(request, 'registration/login.html')


# TODO The page doesnt fit the screen now with the extra umbcid field need to make it bigger or scrollable
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
def delete_account(request):
    user = get_object_or_404(User, pk=request.session['user_id'])
    logout(request)
    user.delete()
    return HttpResponseRedirect('/')


@login_required(login_url='login_user')
def home(request):
	user = ''
	try:
		user = get_object_or_404(User, pk=request.session['user_id'])
	except:
		# will hit here if an admin still logged in tries to use the site this logs him out
		# Weirdly always will show the main page at first but once admin tries to do anything it logs them out
		# and prompts for password
		logout(request)
		HttpResponseRedirect('/login')
	posts = Post.objects.filter(status="active")
	
	post_paginator = Paginator(posts, 5)

	page = request.GET.get('page')

	try:
		post_page = post_paginator.page(page)
	except PageNotAnInteger:
		post_page = post_paginator.page(1)
	except EmptyPage:
		post_page = post_paginator.page(post_paginator.num_pages)

	context = {'user': user, 'post_page': post_page, 'posts': posts}
	return render(request, 'marketplace/home.html', context)

@login_required(login_url='login_user')
def search_results(request):
    user = get_object_or_404(User, pk=request.session['user_id'])

    try:
        good = request.POST['good']
    except:
    	good = "off"

    try:
    	service = request.POST['service']
    except:
    	service = "off"

    if (good == "on" and service == "on") or (good == "off" and service == "off" ):
    	filter_type = "both"
    else:
    	if good == "on":
    		filter_type = "good"
    	else:
    		filter_type = "service"

    try:
    	limit = float(request.POST['limit'])
    except:
    	limit = float(100000000)

    try:

    	if request.POST['free']:
    		try:
    			if filter_type == "both":
    				posts = Post.objects.filter(subject__contains=request.POST['keyword'], cost=0)
    			else:
    				posts = Post.objects.filter(subject__contains=request.POST['keyword'], cost=0, post_type=filter_type)
    		except:
    			if filter_type == "both":
    				posts = Post.objects.all().filter(cost=0)
    			else:
    				posts = Post.objects.all().filter(cost=0, post_type=filter_type)
    except:
    	try:
    		if filter_type == "both":
    			posts = Post.objects.filter(subject__contains=request.POST['keyword'], cost__lte=limit)
    		else:
    			posts = Post.objects.filter(subject__contains=request.POST['keyword'], cost__lte=limit, post_type=filter_type)

    	except:
    		if filter_type == "both":
    			posts = Post.objects.all().filter(cost__lte=limit)
    		else:
    			posts = Post.objects.all().filter(cost__lte=limit, post_type=filter_type) 


    post_paginator = Paginator(posts, 5)

    page = request.GET.get('page')

    try:
    	post_page = post_paginator.page(page)
    except PageNotAnInteger:
    	post_page = post_paginator.page(1)
    except EmptyPage:
    	post_page = post_paginator.page(post_paginator.num_pages)

    context = {'post_page': post_page, 'posts': posts, 'user': user}
    return render(request, 'marketplace/search_results.html', context)


@login_required(login_url='login_user')
def profile(request):
    user = get_object_or_404(User, pk=request.session['user_id'])
    try:
        userstuff = UserModel.objects.get(user=user)
    except:
        return HttpResponse("<html>Shouldnt hit here database needs to be redone.</html>")

    posts = Post.objects.filter(user=user)

    post_paginator = Paginator(posts, 5)
    page = request.GET.get('page')

    try:
        post_page = post_paginator.page(page)
    except PageNotAnInteger:
        post_page = post_paginator.page(1)
    except EmptyPage:
        post_page = post_paginator.page(post_paginator.num_pages)

    edit = request.GET.get('edit')
    ratingcounter = range(0, userstuff.rating)
    missing = range(0, 5 - userstuff.rating)
    context = {'user': user, 'userstuff': userstuff, 'post_page': post_page, 'posts': posts, 'edit': edit, 'ratingcounter': ratingcounter, 'missing': missing}
    return render(request, 'marketplace/profile.html', context)


@login_required(login_url='login_user')
def update_profile(request):
    user = get_object_or_404(User, pk=request.session['user_id'])
    userstuff = get_object_or_404(UserModel, user=user)
    user.first_name = request.POST.get('first')
    user.last_name = request.POST.get('last')
    user.email = request.POST.get('email')
    if request.POST.get('birthday'):
        userstuff.birth_date = request.POST.get('birthday')
    else:
        userstuff.birth_date = None
    userstuff.gender = request.POST.get('gender')
    userstuff.location = request.POST.get('location')

    user.save()
    userstuff.save()
    return HttpResponseRedirect(reverse('profile'))


@login_required(login_url='login_user')
def create_post(request):

    flag = 0;
    user = get_object_or_404(User, pk=request.session['user_id'])
    new_post = Post(user = user, description = request.POST['description'], post_type = request.POST['type'], status="active", creation_date = timezone.now())
    
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

    new_post.post_type = request.POST['type']
    new_post.barter_type = request.POST['barter']

    new_post.save()
    return HttpResponseRedirect(reverse('home'))

@login_required(login_url='login_user')
def view_post(request, post_id):
    user = get_object_or_404(User, pk=request.session['user_id'])
    post = get_object_or_404(Post, pk=post_id)
    seller = post.user
    context = {'post': post, 'seller': seller, 'user': user}
    return render(request, 'marketplace/view_post.html', context)

@login_required(login_url='login_user')
def update_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.subject = request.POST['subject']
    post.description = request.POST['description']
    post.cost = float(request.POST['cost'])
    try:
        post.image = request.FILES['image']
    except:
        pass
    post.save()
    return HttpResponseRedirect(reverse('view_post', args=(post.id, )))

@login_required(login_url='login_user')
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    user = get_object_or_404(User, pk=request.session['user_id'])
    posts = Post.objects.filter(user=user)
    context = {'user': user, 'posts':posts}
    return HttpResponseRedirect(reverse('profile'))


@login_required(login_url='login_user')
def checkout(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {'post': post}
    return render(request, 'marketplace/checkout.html', context)


@login_required(login_url='login_user')
def buy(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.status = "pending"
    buyer = get_object_or_404(User, pk=request.session['user_id'])
    seller = post.user
    new_transaction = Transaction(buyer=buyer, seller=seller, post=post, payment_type = request.POST['payment'], notes=request.POST['notes'], status="active")
    new_transaction.save()
    post.save() 
    return HttpResponseRedirect(reverse('home'))

@login_required(login_url='login_user')
def transactions(request):
    user = get_object_or_404(User, pk=request.session['user_id'])
    purchased = Transaction.objects.filter(buyer=user)
    sold = Transaction.objects.filter(seller=user) 
    context = {'purchased': purchased, 'sold': sold}
    return render(request, 'marketplace/transactions.html', context)

@login_required(login_url='login_user')
def view_transaction(request, transaction_id):
    user = get_object_or_404(User, pk=request.session['user_id'])
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    post = transaction.post
    context = {'transaction': transaction, 'post': post, 'user': user}
    return render(request, 'marketplace/view_transaction.html', context)

@login_required(login_url='login_user')
def relist_post(request, transaction_id):
	try:
		transaction = get_object_or_404(Transaction, pk=transaction_id)
	except:
		return HttpResponseRedirect(reverse('home'))
	transaction.post.status = "active"
	t = Transaction(seller=transaction.seller, buyer=transaction.buyer, post=transaction.post, payment_type=transaction.payment_type, buyerpaid=False, sellerconfirmed=False, status="active")
	t.save()
	transaction.delete()
	return HttpResponseRedirect(reverse('transactions'))

@login_required(login_url='login_user')
def complete_transaction(request, transaction_id):
    user = get_object_or_404(User, pk=request.session['user_id'])
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    post = get_object_or_404(Post, pk=transaction.post.id)
    sellerstuff = get_object_or_404(UserModel, user=transaction.seller)
    buyerstuff = get_object_or_404(UserModel, user=transaction.buyer) 
    if user.pk == transaction.seller.pk:
        transaction.sellerconfirmed = True
        buyerstuff.updateRating(int(request.POST['rating']))
        buyerstuff.save()
    if user.pk == transaction.buyer.pk:
        transaction.buyerpaid = True
        sellerstuff.updateRating(int(request.POST['rating']))
        sellerstuff.save()

    transaction.save() 
    if transaction.sellerconfirmed == True and transaction.buyerpaid == True:
		#c = CompleteTransaction(seller=transaction.seller, buyer=transaction.buyer, postlabel=transaction.post.subject, payment_type=transaction.payment_type, buyerpaid=transaction.buyerpaid, sellerconfirmed=transaction.sellerconfirmed, notes=transaction.notes, status="not active") 
		#c.save()  
		transaction.completed = True
		post.delete()
		#transaction.post = NULL
    return HttpResponseRedirect(reverse('transactions'))

