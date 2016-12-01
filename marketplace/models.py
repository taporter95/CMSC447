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

class Transaction(models.Model):
	seller = models.ForeignKey(User, related_name='seller', on_delete=models.PROTECT)
	buyer = models.ForeignKey(User, related_name='buyer', on_delete=models.PROTECT)
	post = models.ForeignKey(Post, related_name='post', on_delete=models.PROTECT)
	payment_type = models.CharField(max_length=20)
	notes = models.CharField(max_length=200)
	status = models.CharField(max_length=20)

# TODO
class UserModel(models.Model):
    user = models.OneToOneField(User)
    umbcid = models.CharField(max_length=7, primary_key=True)
    rating = models.PositiveSmallIntegerField()

    def __str__(self):
        return "Email: " + str(self.user.username) + \
            "\nPassword: " + str(self.user.password) + \
            "\numbcid: " + str(self.umbcid) + "\nCurrent Rating: " + \
            str(int(self.rating))

    def updateRating(self, rating):
        if rating > 5 or rating < 0:
            return -1
        else:
            self.rating += rating
            self.rating /= 2
