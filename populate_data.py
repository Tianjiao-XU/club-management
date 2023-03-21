import os
import django
from club.models import Club, User, Approval

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cms.settings')


django.setup()


def populate():
    User_Data = [
        {"username": "Fan", "password": "Admin123", "email": "2750565z@student.gla.ac.uk","birthday": "2000-1-18"},
        {"username": "Tianjiao", "password": "Admin123", "email": "2750450x@tudent.gla.ac.uk","birthday": "2001-2-19"},
        {"username": "Haibin", "password": "Admin123", "email": "2757251f@student.gla.ac.uk","birthday": "2002-3-20"},
        {"username": "Tianshuo", "password": "Admin123", "email": "2746520z@student.gla.ac.uk","birthday": "2003-4-21"},
        {"username": "Scott", "password": "Admin123", "email": "2831610i@student.gla.ac.uk", "birthday": "2004-5-22"}
    ]

    Club_Data = [
        {"name": "Velocity", "type": "Sport", "location": "Glasgow",
         "description": "Velocity is a club for people who enjoy participating in sports and staying active. Our members engage in various activities such as running, swimming, and cycling, and participate in local and regional sporting events.",
         "likes": 95, "dislikes": 13},
        {"name": "The Artisans", "type": "Arts & Culture", "location": "London",
         "description": "The Artisans is a club for individuals who appreciate and celebrate the diverse art forms that exist in our world. Our members engage in activities such as attending concerts, visiting museums, and participating in art workshops and exhibitions.",
         "likes": 200, "dislikes": 15},
        {"name": "The Scholars", "type": "Academic", "location": "Manchester",
         "description": "The Scholars is a club for students who value education and strive for academic excellence. Our members engage in various activities such as attending lectures, participating in academic competitions, and engaging in research projects.",
         "likes": 321, "dislikes": 54},
        {"name": "Impact", "type": "Social & Service", "location": "Edinburgh",
         "description": "Impact is a club for individuals who are passionate about making a difference in their communities. Our members engage in various service projects such as volunteering at local non-profits and participating in community service events.",
         "likes": 160, "dislikes": 28},
        {"name": "The Advocates", "type": "Political", "location": "Beijing",
         "description": "The Advocates is a club for individuals who are interested in political issues and are committed to advocating for positive change in their communities. Our members engage in various activities such as attending political rallies, participating in advocacy campaigns, and engaging in political discourse.",
         "likes": 66, "dislikes": 5},
        {"name": "Faithful", "type": "Religious", "location": "Leeds",
         "description": "Faithful is a club for individuals who value their faith and are committed to spiritual growth. Our members engage in various activities such as attending religious services, participating in religious studies, and engaging in charitable work.",
         "likes": 42, "dislikes": 8},
        {"name": "Diversity", "type": "Ethnic", "location": "Shanghai",
         "description": "Diversity is a club for individuals who appreciate and celebrate the diverse cultures that exist in our world. Our members engage in various activities such as attending cultural festivals, participating in cultural workshops, and engaging in cultural exchange programs.",
         "likes": 201, "dislikes": 37},
        {"name": "Paws and Claws", "type": "Animals", "location": "Shenzhen",
         "description": "Paws and Claws is a club for individuals who love animals and are committed to animal welfare. Our members engage in various activities such as volunteering at animal shelters, participating in animal rescue missions, and advocating for animal rights.",
         "likes": 173, "dislikes": 18},
    ]

    for i in range(len(Club_Data)):
        user_instance = add_User(User_Data[i%len(User_Data)])
        club_instance = add_Club(Club_Data[i])
        user_instance.club = club_instance
        user_instance.save()
        club_instance.manager = user_instance
        club_instance.save()

    for i in range(5):
        user = User.objects.get(email=User_Data[i]["email"])
        club = Club.objects.get(name=Club_Data[i+1]["name"])
        approval = Approval.objects.create(user=user, club=club)
        approval.save()


def add_User(user_data):
    user = User.objects.get_or_create(email=user_data["email"])[0]
    user.username = user_data["username"]
    user.set_password(user_data['password'])
    user.birthday = user_data["birthday"]
    user.save()
    return user


def add_Club(club_data):
    club = Club.objects.get_or_create(name=club_data["name"])[0]
    club.type = club_data["type"]
    club.location = club_data["location"]
    club.description = club_data["description"]
    club.likes = club_data["likes"]
    club.dislikes = club_data["dislikes"]
    club.save()
    return club


if __name__ == '__main__':
    print("Initialising simulation data")
    populate()
