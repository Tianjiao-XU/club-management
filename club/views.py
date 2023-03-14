from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
import json
from .models import User, Club, Approval, Comment


def response(code, message="", data=[]):
    result = {"code": code, "message": message, "data": data}
    return HttpResponse(json.dumps(result))


def index(request):
    return render(request, 'club/index.html')


def createClub(request):
    if request.method == "POST":
        user_id = request.session.get('user_id')
        name = request.POST.get("name")
        type = request.POST.get("type")
        location = request.POST.get("location")
        description = request.POST.get("description")

        if not user_id:
            message = "User is not logged in!"
            return response(400, message)
        if not User.objects.get(id=user_id):
            message = "User_id is invalid!"
            return response(400, message)
        if Club.objects.get(name=name):
            message = "CLube name has already been used"
            return response(400, message)

        club = Club(name=name, type=type, location=location, description=description, manager=user_id)
        club.save()
        return render(request, 'club/index.html', locals())


def viewClub(request):
    if request.method == "POST":
        user_id = request.session.get('user_id')
        club_id = request.POST.get("club_id")
        if not user_id:
            message = "User is not logged in!"
            return response(400, message)
        if not User.objects.get(id=user_id):
            message = "User_id is invalid!"
            return response(400, message)
        club = Club.objects.get(id=club_id)
        if not club:
            message = "CLube name has already been used"
            return response(400, message)
        else:
            data = {"name": club["name"], "type": club["type"], "location": club["location"],
                    "description": club["description"], "likes": club["likes"], "dislikes": club["dislikes"]}
        return render(request, 'club/myclub.html', locals())

