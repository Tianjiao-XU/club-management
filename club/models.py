from django.db import models
from django.contrib.auth.models import AbstractUser


class Club(models.Model):
    name = models.CharField(max_length=20, unique=True)
    type = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    manager = models.ForeignKey('User', on_delete=models.SET_NULL,  null=True, blank=True, related_name='managed_clubs')

    class Meta:
        db_table = "Club"

    def __str__(self):
        return self.name


class User(AbstractUser):
    username = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    birthday = models.DateField(blank=True, null=True)
    # club = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    club = models.ManyToManyField(Club)

    REQUIRED_FIELDS = ("username", "password", "birthday")
    USERNAME_FIELD = "email"

    class Meta:
        db_table = "User"


class Approval(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    class Meta:
        db_table = "Approval"

    # def __str__(self):
    #     return self.str(id)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    club = models.ForeignKey(Club, on_delete=models.DO_NOTHING)
    detail = models.CharField(max_length=200)

    class Meta:
        db_table = "Comment"

    def __str__(self):
        return self.id
