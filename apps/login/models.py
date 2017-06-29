from __future__ import unicode_literals
# importing models
from django.db import models
# regex
import re
# bcrypt
import bcrypt
from django.db.models import Count
import datetime
from django.utils import timezone

# checking valid email
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):

    def regVal(self, postData):
        errors = []
        #checks for length in forms
        if len(postData['first_name']) < 2:
            errors.append("First name must be at least 2 characters long")
        if len(postData['last_name']) < 2:
            errors.append("Last name must be at least 2 characters long")
        if not len(postData['email']):
            errors.append("Email must not be blank")
        if len(postData['password']) < 8:
            errors.append("Password must be at least characters 8 long")
        if len(postData['password_cf']) < 8:
            errors.append("Password Confirmation must be at least 8 characters long")
        #checks that passwords match
        if not postData['password'] == postData['password_cf']:
            errors.append("Passwords must match")
        #checks for valid email
        if not EMAIL_REGEX.match(postData['email']):
            errors.append("Email is not valid")
        user = User.objects.filter(email=postData['email'])
        if user:
            errors.append("Email has already been used")

        if len(errors) > 0:
            print "You have errors. Boo!"
            return (False, errors)
        else:
            print "You have 0 errors. Hooray!"
            pw_hash = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(first_name=postData['first_name'], last_name=postData['last_name'], email=postData['email'], password=pw_hash, dob=postData['dob'])
            return (True, user)

    def logVal(self, postData):
        errors2 = []

        if not len(postData['email']):
            errors2.append("Email must not be blank")
        user = User.objects.get(email = postData['email'])
        if not user:
            errors2.append("Invalid email")
        if bcrypt.hashpw(postData['password'].encode(), user.password.encode()) != user.password or len(postData['password']) < 8:
            errors2.append("Incorrect password")

        if len(errors2) > 0:
            print "You have errors. Boo!"
            print "*"*50
            return (False, errors2)
        else:
            print "You have 0 errors. Hooray!"
            print "*"*50
            return (True, user)

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateTimeField(auto_now = True, null = True)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()


class PokeManager(models.Manager):
    # def process_poke(self, postData, user_id):
    #     poke = Poke.objects.create(post = '1', creator = User.objects.get(id=user_id))
    #     return poke

    def process_poke(self, postData, user_id):
        selected_user = User.objects.get(id = postData['user_id'])
        # selected_poke = Poke.objects.get(id = postData['poke_id'])
        # selected_poke.poke.add(selected_user)
        poke = Poke.objects.create(poke = User.objects.get(id='user_id'), poker = User.objects.get(id='user_id'))
        user_pokes = Poke.objects.annotate(num_pokes=Count('poke'))
        return user_pokes

class Poke(models.Model):
    send_user = models.ForeignKey(User, related_name="poker")
    receive_user = models.ForeignKey(User, related_name="pokee")
    poke_date = models.DateTimeField('date poked')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = PokeManager()
