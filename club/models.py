from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify


# club model
class Club(models.Model):
    # name of the club
    name = models.CharField(max_length=20, unique=True)
    # type of the club
    type = models.CharField(max_length=20)
    # location city of the club
    location = models.CharField(max_length=20)
    # description of the club
    description = models.CharField(max_length=200)
    # likes of the club
    likes = models.IntegerField(default=0)
    # dislikes of the club
    dislikes = models.IntegerField(default=0)
    # manager of the club, is a foreign key to the user table
    manager = models.ForeignKey('User', on_delete=models.SET_NULL,  null=True, blank=True, related_name='managed_clubs')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if self.likes < 0:
            self.likes = 0
        if self.dislikes < 0:
            self.dislikes = 0
        super(Club, self).save(*args, **kwargs)

    class Meta:
        db_table = "Club"

    def __str__(self):
        return self.name


# user model, Inherits from Django's built-in AbstractUser model
class User(AbstractUser):
    # username of the user
    username = models.CharField(max_length=20)
    # email of the user
    email = models.EmailField(unique=True)
    # birthday of the user
    birthday = models.DateField(blank=True, null=True)
    # club = models.ForeignKey(Club, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    # Clubs and users are in a many-to-many relationship
    club = models.ManyToManyField(Club)

    REQUIRED_FIELDS = ("username", "password", "birthday")
    USERNAME_FIELD = "email"

    class Meta:
        db_table = "User"


# approval model
class Approval(models.Model):
    # pedning user of the approval, is a foreign key to the user model
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # club of the approval, is a foreign key to the club model
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    # Mark the approval as complete or not
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
