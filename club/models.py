from django.db import models
from django.contrib.auth.models import User

class Club(models.Model):
    name = models.CharField(max_length=20, unique=True)
    type = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    manager = models.ForeignKey('UserProfile', on_delete=models.SET_NULL,  null=True, blank=True, related_name='managed_clubs')

    def __str__(self):
        return self.name


# class User(models.Model):
#     username = models.CharField(max_length=20)
#     password = models.CharField(max_length=20)
#     email = models.EmailField(unique=True)
#     birthday = models.DateField(blank=True, null=True)
#     club = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
#
#     def __str__(self):
#         return self.email


# class Approval(models.Model):
#     user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
#     club = models.ForeignKey(Club, on_delete=models.DO_NOTHING)
#     completed = models.BooleanField(default=0)
#
#     def __str__(self):
#         return self.id
#
#
# class Comment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
#     club = models.ForeignKey(Club, on_delete=models.DO_NOTHING)
#     detail = models.CharField(max_length=200)
#
#     def __str__(self):
#         return self.id

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    birthday = models.DateField(blank=True, null=True)
    club = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    def __str__(self):
        return self.user.username
