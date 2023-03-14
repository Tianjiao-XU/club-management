import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cms.settings')

import django
django.setup()
from club.models import Club,User,UserProfile

def populate():

    User = [
        {"username":"k1","password":"123123" ,"email": "1@qq.com","birthday":"2000-01-01"},
        {"username":"k2","password":"123123" ,"email": "2@qq.com","birthday":"2000-01-01"},
        {"username":"k3","password":"123123" ,"email": "3@qq.com","birthday":"2000-01-01"},
    ]

    Club = [
        {"name":"a_club","type":"basketball" ,"location":"Glasgow" ,"description":"I like basketball" ,"likes":1 ,"dislikes":1},
        {"name":"b_club","type":"football" ,"location":"London" ,"description":"I like football" ,"likes":2 ,"dislikes":2},
        {"name":"c_club","type":"boxing" ,"location":"ShenZhen" ,"description":"I like boxing" ,"likes":3 ,"dislikes":3},
    ]

    # UserProfile = [
    #     {},
    #
    # ]

    for i in User:
        add_User(i)

    for i in Club:
        add_Club(i)


def add_User(user_data):
    user = User.objects.get_or_create(email=user_data["email"])[0]
    user.username = user_data["username"]
    user.password = user_data["password"]
    user.birthday = user_data["birthday"]
    user.save()


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