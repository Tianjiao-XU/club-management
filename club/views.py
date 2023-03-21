from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from club.models import User, Club, Approval
from club.forms import RegisterForm, LoginForm, CreateClubForm
import json
from django.contrib.sessions.backends.db import SessionStore


def general_response(code, message="", data=[]):
    result = {"code": code, "message": message, "data": data}
    return HttpResponse(json.dumps(result))


def index(request):
    #request.session.set_test_cookie()
    # visitor_cookie_handler(request)
    # context_dict['visits'] = request.session['visits']
    club_list  = Club.objects.order_by('-likes')[:3]
    context_dict = {'club_list':club_list}
    response = render(request, 'club/index.html', context_dict)
    return response


@login_required(login_url="/club/login")
def evaluateClub(request, club_id):
    club = Club.objects.get(id=club_id)
    if not club:
        messages.error(request, "Club does not exist!")
        club_list = request.user.club.all()
        return render(request, 'club/myclublist.html', {"club_list": club_list})
    if request.method == 'POST':
        choice = request.POST.get('evaluate')
        if choice == 'like':
            club.likes += 1
        else:
            club.dislikes += 1
        club.save()
    return render(request, 'club/myclubevaluate.html', {"club": club})


@login_required(login_url="/club/login")
def likeordislikeClub(request):
    club_id = request.POST.get("club_id")
    club = Club.objects.get(id=club_id)
    if not club:
        messages.error(request, "Club does not exist!")
        club_list = request.user.club.all()
        return render(request, 'club/myclublist.html', {"club_list": club_list})
    choice = request.POST.get('evaluate')
    if choice == 'like':
        club.likes += 1
    else:
        club.dislikes += 1
    club.save()
    member_list = User.objects.filter(club=club)
    return render(request, 'club/clubdetails.html', {"member_list": member_list, "club": club})


@login_required(login_url="/club/login")
def manageClub(request, club_id):
    club = Club.objects.get(id=club_id)
    if not club:
        messages.error(request, "Club does not exist!")
        club_list = request.user.club.all()
        return render(request, 'club/myclublist.html', {"club_list": club_list})
    approval_list = Approval.objects.filter(club=club, completed=0)
    return render(request, 'club/myclubmanage.html', {"approval_list": approval_list, "club": club})


@login_required(login_url="/club/login")
def dealApproval(request):
    if request.method == 'POST':
        user = request.user
        approval_id = request.POST.get("approval_id")
        app = Approval.objects.get(id=approval_id)
        if not app:
            messages.error(request, "Approval does not exist!")
            club_list = user.club.all()
            return render(request, 'club/myclublist.html', {"club_list": club_list})
        club = Club.objects.get(id=app.club_id)
        if not club:
            messages.error(request, "Club does not exist!")
            club_list = request.user.club.all()
            return render(request, 'club/myclublist.html', {"club_list": club_list})
        pending_user = User.objects.get(id=app.user_id)
        if not pending_user:
            messages.error(request, "Club does not exist!")
            approval_list = Approval.objects.filter(club=club, completed=0)
            return render(request, 'club/myclubmanage.html', {"approval_list": approval_list, "club": club})
        approval = request.POST.get("approval")
        if user == club.manager:
            if approval == "approve":
                pending_user.club.add(club)
                app.completed = 1
                app.save()
            elif approval == "reject":
                app.completed = 1
                app.save()
            else:
                messages.error(request, "Approval is not valid!")
                approval_list = Approval.objects.filter(club=club, completed=0)
                return render(request, 'club/myclubmanage.html', {"approval_list": approval_list, "club": club})
        else:
            messages.error(request, 'you are not the manager')
        approval_list = Approval.objects.filter(club=club, completed=0)
        return render(request, 'club/myclubmanage.html', {"approval_list": approval_list, "club": club})


def contact(request):
    return render(request, 'club/contact.html')


@login_required(login_url="/club/login")
def myclublist(request):
    club_list = request.user.club.all()
    return render(request, 'club/myclublist.html', {"club_list": club_list})


def register(request):
    registered = False
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # Save the register form data to the database.
            user = register_form.save()
            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Update our variable to indicate that the template
            # registration was successful.
            registered = True
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        register_form = RegisterForm()

    # Render the template depending on the context.
    return render(request, 'club/register.html', context={'register_form': register_form, 'registered': registered})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('/club/')
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            email = login_form.cleaned_data['email']
            login(request, user)
            request.session['email'] = email
            return redirect(reverse('club:index'))
    else:
        login_form = LoginForm()
    return render(request, 'club/login.html', {'login_form': login_form})


def search(request):
    if request.method == 'POST':
        key = request.POST.get("key")
        if not key:
            messages.error(request, "Search input is empty!")
            return render(request, 'club/search.html')
        results = list(Club.objects.filter(name__icontains=key))
        if not results:
            results = list(Club.objects.filter(type__icontains=key))
            if not results:
                results = list(Club.objects.filter(location__icontains=key))
        return render(request, 'club/search.html', {"clubs": results})
    return render(request, 'club/search.html')


# def logout(request):
#     if not request.user.is_authenticated():
#         return HttpResponse("You are logged in")
#     else:
#         return HttpResponse("You are not logged in")
# Use the login_required() decorator to ensure only those logged in can
# access the view.

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('club:index'))


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


# an example for deal with cookies(copy from book)
def visitor_cookie_handler(request):
    # Get the number of visits to the site.
    # We use the COOKIES.get() function to obtain the visits cookie.
    # If the cookie exists, the value returned is casted to an integer.
    # If the cookie doesn't exist, then the default value of 1 is used.
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    # last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
    last_visit_cookie = get_server_side_cookie(request,'last_visit',str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')
    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).seconds > 0:
        visits = visits + 1
        # Update the last visit cookie now that we have updated the count
        #     response.set_cookie('last_visit', str(datetime.now()))
        request.session['last_visit'] = str(datetime.now())
    else:
        # Set the last visit cookie
        #     response.set_cookie('last_visit', last_visit_cookie)
        request.session['last_visit'] = last_visit_cookie

    # Update/set the visits cookie
    # response.set_cookie('visits', visits)
    request.session['visits'] = visits


@login_required(login_url="/club/login")
def createClub(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            club_form = CreateClubForm(request.POST)
            if club_form.is_valid():
                club = club_form.save()
                club.manager = request.user
                club.save()
                user = request.user
                user.club.add(club)
                return redirect('/club/')
        else:
            club_form = CreateClubForm()
        return render(request, 'club/create_club.html', {'club_form': club_form})
    else:
        messages.error(request, 'Please log in first!')
        return redirect('/club/login')


@login_required(login_url="/club/login")
def viewClub(request, club_id):
    if request.user.is_authenticated:
        club = Club.objects.get(id=club_id)
        if not club:
            messages.error(request, "Club does not exist!")
            club_list = request.user.club.all()
            return render(request, 'club/myclublist.html', {"club_list": club_list})
        else:
            member_list = User.objects.filter(club=club)
            return render(request, 'club/clubdetails.html', {"member_list":member_list,"club":club})
    else:
        messages.error(request, 'Please log in first!')
        return redirect('/club/login')


@login_required(login_url="/club/login")
def joinClub(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            club_id = request.POST.get("club_id")
            if not Club.objects.filter(id=club_id).first():
                messages.error(request, "Club does not exist!")
                return render(request, 'club/search.html')
            user = User.objects.get(id=request.user.id)
            approval = Approval(club_id=club_id, user=user)
            approval.save()
            return redirect("/club/")
    else:
        messages.error(request, 'Please log in first!')
        return redirect('/club/login')


@login_required(login_url="/club/login")
def removeMember(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            member_id = request.POST.get("member_id")
            club_id = request.POST.get("club_id")
            club = Club.objects.get(id=club_id)
            if not club:
                messages.error(request, "Club does not exist!")
                club_list = request.user.club.all()
                return render(request, 'club/myclublist.html', {"club_list": club_list})
            member = User.objects.get(id=member_id)
            if not member:
                messages.error(request, "Member does not exist!")
                member_list = User.objects.filter(club=club)
                return render(request, 'club/clubdetails.html', {"member_list": member_list, "club": club})
            if club not in member.club.all():
                messages.error(request, "User "+member.username+"is not a member of the club!")
                member_list = User.objects.filter(club=club)
                return render(request, 'club/clubdetails.html', {"member_list": member_list, "club": club})

            member.club.remove(club)
            member_list = User.objects.filter(club=club)
            return render(request, 'club/clubdetails.html', {"member_list": member_list, "club": club})
    else:
        messages.error(request, 'Please log in first!')
        return redirect('/club/login')