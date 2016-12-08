from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200, db_index=True)
    description = models.CharField(max_length=200)
    cost = models.FloatField(default=0)
    image = models.FileField(null=True, blank=True, upload_to='uploads/')
    post_type = models.CharField(max_length=20)
    barter_type = models.CharField(max_length=20)
    creation_date = models.DateTimeField(db_index=True)
    status = models.CharField(max_length=20)
    hourly = models.BooleanField(default=False)

class Transaction(models.Model):
	seller = models.ForeignKey(User, related_name='seller')
	buyer = models.ForeignKey(User, related_name='buyer')
	post = models.ForeignKey(Post, related_name='post')
	payment_type = models.CharField(max_length=64) # Represents payment method i.e cash on delivery, barter, service..etc
	buyerpaid = models.BooleanField(default=False)
	sellerconfirmed = models.BooleanField(default=False)
	notes = models.CharField(max_length=200)
	status = models.CharField(max_length=20)
	completed = models.BooleanField(default=False)
	seller_read = models.BooleanField(default=False)
	buyer_read = models.BooleanField(default=False)
	seller_relisted = models.BooleanField(default=False)
	buyer_canceled = models.BooleanField(default=False)
	def __str__(self):
		return "Seller: " + str(self.seller) + \
            "\Payment Method: " + str(self.payment_type) + \
            "\nHas the buyer paid: " + str(self.buyerpaid) + "\nHas the seller confirmed: " + \
            str(int(self.sellerconfirmed))

#class CompleteTransaction(models.Model):
#    seller = models.CharField(max_length=200)
#    buyer = models.CharField(max_length=200)
#    postlabel = models.CharField(max_length=200)
#    payment_type = models.CharField(max_length=64) # Represents payment method i.e cash on delivery, barter, service..etc
#    buyerpaid = models.BooleanField(default=False)
#    sellerconfirmed = models.BooleanField(default=False)
#    notes = models.CharField(max_length=200)
#    status = models.CharField(max_length=20)

#    def __str__(self):
#    	return "\nSeller: " + str(self.seller) + \
#			"\nBuyer: " + str(self.buyer) + \
#			"\npostLabel: " + str(self.postlabel) + \
#            "\nPayment Method: " + str(self.payment_type) + \
#            "\nHas the buyer paid: " + str(self.buyerpaid) + "\nHas the seller confirmed: " + \
#            str(self.sellerconfirmed) + \
#			"\nNotes: " + str(self.notes) + \
#			"\nstatus: " + str(self.status)


    # TODO
class UserModel(models.Model):
    
	MALE = 'M'
	FEMALE = 'F'
	OTHER = 'O'
	GENDER_CHOICES = (
		(MALE, 'Male'),
		(FEMALE, 'Female'),
		(OTHER, 'Other'),
	)
    
	user = models.OneToOneField(User)
	umbcid = models.CharField(max_length=7, primary_key=True)
	rating = models.PositiveSmallIntegerField(default=5)
	birth_date = models.DateField(null=True, blank=True)
	gender = models.CharField(max_length=8, blank=True)
	location = models.CharField(max_length=200, blank=True)
	banned = models.BooleanField(default=False)

	def __str__(self):
		return "Email: " + str(self.user.username) + \
			"\nPassword: " + str(self.user.password) + \
			"\numbcid: " + str(self.umbcid) + "\nCurrent Rating: " + \
			str(int(self.rating))

	def getDateForHTML(self):
		if self.birth_date:
			return self.birth_date.strftime("%Y-%m-%d")
		else:
			return ""
    
	def updateRating(self, rating):
		if rating > 5 or rating < 0:
			return -1
		else:
			self.rating += rating
			self.rating /= 2
			self.rating = int(self.rating)


