import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cms.settings')

import django

django.setup()
from club.models import Club, User

# from django.contrib.auth.models import User


def populate():
    User_Data = [
        {"username": "k2", "password": "123123", "email": "2@qq.com","birthday": "2001-1-18"},
        {"username": "k3", "password": "123123", "email": "3@qq.com","birthday": "2002-1-18"},
        {"username": "k4", "password": "123123", "email": "4@qq.com","birthday": "2003-1-18"},
    ]

    Club_Data = [
        {"name": "a_club", "type": "basketball", "location": "Glasgow", "description": "I like basketball", "likes": 1,
         "dislikes": 1},
        {"name": "b_club", "type": "football", "location": "London", "description": "I like football", "likes": 2,
         "dislikes": 2},
        {"name": "c_club", "type": "boxing", "location": "ShenZhen", "description": "I like boxing", "likes": 3,
         "dislikes": 3},
    ]

    # UserProfile_Data = [
    #     {"birthday": "2001-1-18", "website": "www.1399.com","picture":"profile_images/cat.jpg"},
    #     {"birthday": "2002-10-18", "website": "www.2399.com"},
    #     {"birthday": "2003-10-18", "website": "www.3399.com"},
    #
    # ]

    for i in range(len(User_Data)):
        user_instance = add_User(User_Data[i])
        # add_UserProfile(user_instance, UserProfile_Data[i])

    for i in Club_Data:
        add_Club(i)


def add_User(user_data):
    user = User.objects.get_or_create(email=user_data["email"])[0]
    user.username = user_data["username"]
    user.set_password(user_data['password'])
    user.birthday = user_data["birthday"]
    user.save()
    # return user


# def add_UserProfile(User, userProfile_data):
#     userprofile = UserProfile.objects.get_or_create(user=User)[0]
#     userprofile.user = User
#     userprofile.birthday = userProfile_data['birthday']
#     userprofile.website = userProfile_data['website']
#     userprofile.picture = userProfile_data.get('picture')
#     userprofile.save()


def add_Club(club_data):
    club = Club.objects.get_or_create(name=club_data["name"])[0]
    club.type = club_data["type"]
    club.location = club_data["location"]
    club.description = club_data["description"]
    club.likes = club_data["likes"]
    club.dislikes = club_data["dislikes"]
    club.save()


if __name__ == '__main__':
    print("加载模拟数据")
    populate()
