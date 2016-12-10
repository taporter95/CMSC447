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
from itertools import chain
import datetime
import calendar
import random
import re



#get the number of transaction objects marked as unread
def get_unread(user):

	set_1 = Transaction.objects.filter(buyer=user, completed=False, buyer_read=False).count()
	set_2 = Transaction.objects.filter(seller=user, completed=False, seller_read=False).count()
	
	return set_1 + set_2


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
	    if userstuff is None: #if user does not exist
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


def new_user(request):
	return render(request, 'registration/new_user.html')


def create_user(request):
	#match regex for email
	if re.match(r'^[\w]+@umbc\.edu$', request.POST['email']):
	    pass
	else:
	    messages.add_message(request, messages.ERROR, 'You must have a valid UMBC email')
	    return HttpResponseRedirect(reverse('new_user'))
	   
	#match regex for ID 
	if re.match('[A-Z][A-Z][0-9][0-9][0-9][0-9][0-9]', request.POST['umbcid'].upper()):
	    pass
	else:
	    messages.add_message(request, messages.ERROR, 'You must have a valid UMBC Id')
	    return HttpResponseRedirect(reverse('new_user'))

	#check password
	if request.POST['password'] != request.POST['repassword']:
	    messages.add_message(request, messages.ERROR, 'Passwords do not match')
	    return HttpResponseRedirect(reverse('new_user'))

	#create new user if it does not exist
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
	#get posts
	posts = Post.objects.filter(status="active").order_by('-creation_date')
	#set up pagination
	post_paginator = Paginator(posts, 5)

	page = request.GET.get('page')

	try:
		post_page = post_paginator.page(page)
	except PageNotAnInteger:
		post_page = post_paginator.page(1)
	except EmptyPage:
		post_page = post_paginator.page(post_paginator.num_pages)

	unread = get_unread(user)

	context = {'user': user, 'unread': unread, 'post_page': post_page, 'posts': posts}
	return render(request, 'marketplace/home.html', context)

@login_required(login_url='login_user')
def search_results(request):
	user = get_object_or_404(User, pk=request.session['user_id'])
	unread = get_unread(user)

	#Does user want to see goods, services, or both
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

	#filter based on search parameters
	try:
		if request.POST['free']:
			try:
				if filter_type == "both":
					posts = Post.objects.filter(subject__contains=request.POST['keyword'], cost=0, status="active").order_by('-creation_date')
				else:
					posts = Post.objects.filter(subject__contains=request.POST['keyword'], cost=0, post_type=filter_type, status="active").order_by('-creation_date')
			except:
				if filter_type == "both":
					posts = Post.objects.all().filter(cost=0, status="active").order_by('-creation_date')
				else:
					posts = Post.objects.all().filter(cost=0, post_type=filter_type, status="active").order_by('-creation_date')
	except:
		try:
			if filter_type == "both":
				posts = Post.objects.filter(subject__contains=request.POST['keyword'], cost__lte=limit, status="active").order_by('-creation_date')			
			else:
				posts = Post.objects.filter(subject__contains=request.POST['keyword'], cost__lte=limit, post_type=filter_type, status="active").order_by('-creation_date')

		except:
			if filter_type == "both":
				posts = Post.objects.all().filter(cost__lte=limit, status="active").order_by('-creation_date')
			else:
				posts = Post.objects.all().filter(cost__lte=limit, post_type=filter_type, status="active").order_by('-creation_date')

	#set up pagination
	post_paginator = Paginator(posts, 5)

	page = request.GET.get('page')

	try:
		post_page = post_paginator.page(page)
	except PageNotAnInteger:
		post_page = post_paginator.page(1)
	except EmptyPage:
		post_page = post_paginator.page(post_paginator.num_pages)

	context = {'post_page': post_page, 'unread': unread, 'posts': posts, 'user': user}
	return render(request, 'marketplace/search_results.html', context)


@login_required(login_url='login_user')
def profile(request, user_id):
	current_profile = get_object_or_404(User, pk=user_id)
	user = get_object_or_404(User, pk=request.session['user_id'])
	actual = user

	#check to see if the current user is viewing their profile or someone else's
	if current_profile != user:
	    user = current_profile

	unread = get_unread(actual)

	try:
	    userstuff = UserModel.objects.get(user=user)
	except:
	    return HttpResponse("<html>Shouldnt hit here database needs to be redone.</html>")

	posts = Post.objects.filter(user=user, status="active").order_by('-creation_date')

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
	context = {'user': user, 'actual': actual, 'unread': unread, 'userstuff': userstuff, 'post_page': post_page, 'posts': posts, 'edit': edit, 'ratingcounter': ratingcounter, 'missing': missing}
	return render(request, 'marketplace/profile.html', context)


@login_required(login_url='login_user')
def update_profile(request):
	#get user and update fields
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
	return HttpResponseRedirect(reverse('profile', args=(user.id, )))


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
	
	try:
		if request.POST['hourly'] == "on":
			new_post.hourly = True
	except:
		pass

	new_post.post_type = request.POST['type']
	new_post.barter_type = request.POST['barter']

	new_post.save()
	return HttpResponseRedirect(reverse('home'))

@login_required(login_url='login_user')
def view_post(request, post_id):
	user = get_object_or_404(User, pk=request.session['user_id'])
	unread = get_unread(user)
	post = get_object_or_404(Post, pk=post_id)
	seller = post.user
	context = {'post': post, 'unread': unread, 'seller': seller, 'user': user}
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
	return HttpResponseRedirect(reverse('profile', args=(user.id, )))


@login_required(login_url='login_user')
def checkout(request, post_id):
	post = get_object_or_404(Post, pk=post_id)
	user = get_object_or_404(User, pk=request.session['user_id'])
	unread = get_unread(user)
	context = {'post': post, 'unread': unread}
	return render(request, 'marketplace/checkout.html', context)


@login_required(login_url='login_user')
def buy(request, post_id):
	post = get_object_or_404(Post, pk=post_id)
	post.status = "pending"
	buyer = get_object_or_404(User, pk=request.session['user_id'])
	seller = post.user
	#create a new transaction object to store information
	new_transaction = Transaction(buyer=buyer, seller=seller, post=post, payment_type = request.POST['payment'], notes=request.POST['notes'], status="active")
	new_transaction.save()
	post.save() 
	return HttpResponseRedirect(reverse('home'))

@login_required(login_url='login_user')
def transactions(request):
	user = get_object_or_404(User, pk=request.session['user_id'])
	unread = get_unread(user)
	purchased_active = Transaction.objects.filter(buyer=user, completed=False, status="active")
	purchased_canceled = Transaction.objects.filter(buyer=user, completed=False, status="canceled")
	#merge the lists of active and canceled transactions
	purchased = list(chain(purchased_active, purchased_canceled))
	
	sold_active = Transaction.objects.filter(seller=user, completed=False, status="active") 
	sold_canceled = Transaction.objects.filter(seller=user, completed=False, status="canceled") 
	#merge the lists of active and canceled transactions
	sold = list(chain(sold_active, sold_canceled))
	context = {'purchased': purchased, 'sold': sold, 'unread': unread} 
	return render(request, 'marketplace/transactions.html', context)

@login_required(login_url='login_user')
def view_transaction(request, transaction_id):
	user = get_object_or_404(User, pk=request.session['user_id'])
	transaction = get_object_or_404(Transaction, pk=transaction_id)
	#mark that the user has viewed this transaction
	if user == transaction.seller:
		transaction.seller_read = True
	else:
		transaction.buyer_read = True

	transaction.save()
	unread = get_unread(user)
	post = transaction.post
	context = {'transaction': transaction, 'post': post, 'user': user, 'unread': unread}
	return render(request, 'marketplace/view_transaction.html', context)

@login_required(login_url='login_user')
def relist_post(request, transaction_id):
	user = get_object_or_404(User, pk=request.session['user_id'])

	try:
		transaction = get_object_or_404(Transaction, pk=transaction_id)
	except:
		return HttpResponseRedirect(reverse('home'))

	#set flags for notifications
	if user == transaction.seller:
		transaction.buyer_read = False
		transaction.sellerconfirmed = True
		transaction.seller_relisted = True
		transaction.save()
	else:
		transaction.seller_read = False
		transaction.buyerpaid = True
		transaction.buyer_canceled = True
		transaction.save()

	transaction.post.status = "active"
	transaction.post.save()
	
	transaction.status = "canceled"
	transaction.save()
	return HttpResponseRedirect(reverse('transactions'))

@login_required(login_url='login_user')
def complete_transaction(request, transaction_id):
	user = get_object_or_404(User, pk=request.session['user_id'])
	transaction = get_object_or_404(Transaction, pk=transaction_id)
	post = get_object_or_404(Post, pk=transaction.post.id)
	sellerstuff = get_object_or_404(UserModel, user=transaction.seller)
	buyerstuff = get_object_or_404(UserModel, user=transaction.buyer) 
	if user.pk == transaction.seller.pk and transaction.sellerconfirmed == False:
		transaction.sellerconfirmed = True
		transaction.buyer_read = False
		try:
			buyerstuff.updateRating(int(request.POST['rating']))
			buyerstuff.save()
		except:
			pass

	if user.pk == transaction.buyer.pk and transaction.buyerpaid == False:
		transaction.buyerpaid = True
		transaction.seller_read = False
		try:
			sellerstuff.updateRating(int(request.POST['rating']))
			sellerstuff.save()
		except:
			pass

	transaction.save() 
	if transaction.sellerconfirmed == True and transaction.buyerpaid == True: 
		transaction.completed = True
		if transaction.buyer_canceled == True or transaction.seller_relisted == True:
			post.status = "active"
		else:
			post.status = "inactive"

		transaction.save()
		post.save()
	return HttpResponseRedirect(reverse('transactions'))

