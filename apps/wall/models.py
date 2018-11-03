from __future__ import unicode_literals
from django.db import models

import re, bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
name_regex = re.compile(r'^[a-zA-Z]+$')


class UserManager(models.Manager):

    def register_validate(self, postData):
        errors = {}
        a = User.objects.filter(email = postData['email'])
        
        if len(postData["first_name"]) < 2:
            errors["first_name"] = "First name should be at least 2 characters."
        elif not name_regex.match(postData['first_name']):
            errors["first_name"] = "First name should contain only letters."

        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters."
        elif not name_regex.match(postData['last_name']):
            errors["last_name"] = "Last name should contain only letters."

        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid e-mail address."
        elif a:
            errors["email"] = "The email already exists in our system. Please type another one."

        if len(postData['password']) < 1:
            errors["password"] = "Please enter your password."
        elif len(postData['password']) < 8:
            errors["password"] = "Password should be more than 8 characters long."
        elif re.search('[0-9]', postData['password']) is None:
            errors["password"] = "Make sure that your password has a number in it." 
        elif re.search('[A-Z]', postData['password']) is None: 
            errors["password"] = "Make sure that your password has a capital letter in it."
        
        if len(postData["password_con"]) < 1:
            errors["password_con"] = "Please verify your password."
        elif postData["password_con"] != postData['password']:
            errors["password_con"] = "The passwords do not match."
        return errors
    
    def login_validate(self, postData):
        user = User.objects.filter(email = postData['email'])
        errors = {}

        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid e-mail address."
        if len(postData['password']) < 1:
            errors["password"] = "Please enter your password."
        elif len(user) == 0:
            errors["password"] = "Cannot find e-mail address in our system. Please register."
        elif not bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
            errors["password"] = "Incorrect password. Please try again."

        return errors
    
    def success(self):
        message = {}
        message['register'] = "You have successfully registered!"
        message['login'] = "You have successfully logged in!"

        return message
    
    def post_validate(self, postData):
        errors = {}
        if len(postData['message']) < 10:
            errors["message"] = "Message must be more than ten characters long."
        return errors
    
    def comment_validate(self, postData):
        errors = {}
        if len(postData['comment']) < 5:
            errors["comment"] = "Comment must be more than five characters long."
        return errors


class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Message(models.Model):
    message = models.TextField(max_length = 1000)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    user = models.ForeignKey(User, related_name = "messages")

class Comment(models.Model):
    comment = models.TextField(max_length = 1000)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    user = models.ForeignKey(User, related_name = "comments")
    message = models.ForeignKey(Message, related_name = "comments")
