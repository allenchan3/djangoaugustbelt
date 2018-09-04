from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re, bcrypt
# Create your models here.

email_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]*$')

class UserManager(models.Manager):
    def register(self, form_data):
        
        errors = []
        
        if len(form_data["first_name"]) < 1:
            errors.append("First Name is required")
        elif len(form_data["first_name"]) < 3:
            errors.append("First Name must be 2 letters or longer")
        
        if len(form_data["email"]) < 1:
            errors.append("Username is required")
        elif len(form_data["email"]) < 3:
            errors.append("Invalid Username")
        else:
            if len(User.objects.filter(email=form_data["email"])) > 0:
                errors.append("Username already in use")

        if len(form_data["password"]) < 1:
            errors.append("Password is required")
        elif len(form_data["password"]) < 8:
            errors.append("Password must be 8 letters or longer")
        
        if len(form_data["confirm_password"]) < 1:
            errors.append("Confirm Password is required")
        elif form_data["confirm_password"] != form_data["password"]:
            errors.append("Confirm Password must match Password")

        if len(errors) == 0:    
            hashed_pw = bcrypt.hashpw(form_data["password"].encode(), bcrypt.gensalt())
            user = User.objects.create(
                first_name= form_data["first_name"],
                birthday= form_data["dob"],
                email= form_data["email"],
                password= hashed_pw
            )
            return (True, user)
        else:
            return (False,errors)

    def login(self, form_data):

        errors = []

        if len(form_data["email"]) < 1:
            errors.append("Username is required")
        elif len(form_data["email"]) < 3:
            errors.append("Invalid Username")
        else:
            if len(User.objects.filter(email=form_data["email"])) < 1:
                errors.append("Unknown Username {}".format(form_data["email"]))
        
        if len(form_data["password"]) < 1:
                errors.append("Password is required")
        elif len(form_data["password"]) < 8:
            errors.append("Password must be 8 letters or longer")

        if len(errors) > 0:
            return(False, errors)

        user = User.objects.filter(email=form_data["email"])[0]
        
        if bcrypt.checkpw(form_data["password"].encode(), user.password.encode()):
            return (True, user)
        else:
            errors.append("Incorrect password")
            return (False, errors)        

class ItemManager(models.Manager):
    def add_item(self, formData):
        response = {
            'errors':[],
            }
        if len(formData['title']) < 3:
            response["errors"].append("Item is too short!")
        
        if len(response['errors']) > 0:
            return(False, response, None)

        response['success'] = "Items Added!"
        
    
        return (True, response, Itemlist)

class User(models.Model):
    first_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    birthday= models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    objects = UserManager()

class Itemlist(models.Model):
    title = models.CharField(max_length=255)
    item_added_by = models.ForeignKey(User, related_name= 'items_user_added')
    item_favorited_by_users = models.ManyToManyField(User,related_name="user_favorite_items")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    objects = ItemManager()