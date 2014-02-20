from django.db import models
from django import forms

# Create your models here.

# User model
class UserModel(models.Model):

    SUCCESS = 1
    ERR_BAD_CREDENTIALS = -1
    ERR_USER_EXISTS = -2
    ERR_BAD_USERNAME = -3
    ERR_BAD_PASSWORD = -4
    MAX_USERNAME_LENGTH = 128
    MAX_PASSWORD_LENGTH = 128

    username = models.CharField(max_length = MAX_USERNAME_LENGTH)
    password = models.CharField(max_length = MAX_PASSWORD_LENGTH, default = "")
    count = models.IntegerField(default = 0)

    def __unicode__(self):
        return self.username

    @staticmethod
    def login(user, passw):
        u = UserModel.objects.filter(username = user)
        if len(u) != 1 or u[0].password != passw:
            return UserModel.ERR_BAD_CREDENTIALS
        else:
            u[0].count += 1
            u[0].save()
            return UserModel.SUCCESS

    @staticmethod
    def add(user, passw):
        if len(user) == 0 or len(user) > UserModel.MAX_USERNAME_LENGTH:
            return UserModel.ERR_BAD_USERNAME
        elif len(passw) > UserModel.MAX_PASSWORD_LENGTH:
            return UserModel.ERR_BAD_PASSWORD
        elif len(UserModel.objects.filter(username = user)) > 0:
            return UserModel.ERR_USER_EXISTS
        else:
            u = UserModel(username = user, password = passw, count = 1)
            u.save()
            return UserModel.SUCCESS

class UserForm(forms.Form):
    username = forms.CharField()
    passwd = forms.CharField(widget = forms.PasswordInput())