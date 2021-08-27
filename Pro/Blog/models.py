from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BlogPost(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateField()
    author = models.CharField(max_length=50)

    def __str__(self):
        return f"Author : {self.author} and Title : {self.title}"

class Contact(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    number = models.CharField(max_length=20)
    message = models.TextField()

    def __str__(self):
        return f"Name : {self.name} and Message : {self.message}"


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    forgot_pass_token = models.CharField(max_length=100,default='')
    is_verified = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username