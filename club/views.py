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


def general_response(code, message="", data=[]):
    result = {"code": code, "message": message, "data": data}
    return HttpResponse(json.dumps(result))


def index(request):
    # show the homepage function
    # Get the top three clubs with the highest number of likes, in descending order of number of likes
    club_list = Club.objects.order_by('-likes')[:3]
    # return the clubs list
    context_dict = {'club_list':club_list}
    response = render(request, 'club/index.html', context_dict)
    return response


@login_required(login_url="/club/login")
def evaluateClub(request, club_id):
    # show the club evaluation page
    # get the club according to the club_id
    club = Club.objects.get(id=club_id)
    if not club:
        # if club does not exist, return error, redirect to myclublist page
        messages.error(request, "Club does not exist!")
        club_list = request.user.club.all()
        return render(request, 'club/myclublist.html', {"club_list": club_list})
    # return the club details and redirect to evaluate club page
    return render(request, 'club/myclubevaluate.html', {"club": club})


@login_required(login_url="/club/login")
def likeordislikeClub(request):
    # evaluate the club function
    if request.method == 'POST':
        # get the club according to the club_id
        club_id = request.POST.get("club_id")
        club = Club.objects.get(id=club_id)
        if not club:
            # if club does not exist, return error, redirect to myclublist page
            messages.error(request, "Club does not exist!")
            club_list = request.user.club.all()
            return render(request, 'club/myclublist.html', {"club_list": club_list})
        # get the evaluation choice
        choice = request.POST.get('evaluate')
        # update club information according to the choice
        if choice == 'like':
            club.likes += 1
        else:
            club.dislikes += 1
        club.save()
        # return the latest information of the club and redirect to club details page
        member_list = User.objects.filter(club=club)
        return render(request, 'club/clubdetails.html', {"member_list": member_list, "club": club})


@login_required(login_url="/club/login")
def manageClub(request, club_id):
    # manage club page
    club = Club.objects.get(id=club_id)
    if not club:
        # if club does not exist, return error, redirect to myclublist page
        messages.error(request, "Club does not exist!")
        club_list = request.user.club.all()
        return render(request, 'club/myclublist.html', {"club_list": club_list})
    # get the approval list and return it with the club detail
    approval_list = Approval.objects.filter(club=club, completed=0)
    return render(request, 'club/myclubmanage.html', {"approval_list": approval_list, "club": club})


@login_required(login_url="/club/login")
def dealApproval(request):
    # approve or disapprove the join request function
    if request.method == 'POST':
        # get current user
        user = request.user
        # get approval id from request.POST and get the Approval model
        approval_id = request.POST.get("approval_id")
        app = Approval.objects.get(id=approval_id)
        if not app:
            # if approval does not exist, return error, redirect to myclublist page
            messages.error(request, "Approval does not exist!")
            club_list = user.club.all()
            return render(request, 'club/myclublist.html', {"club_list": club_list})
        if app.completed:
            # if approval has been completed, return error, redirect to myclublist page
            messages.error(request, "Approval has been completed!")
            club_list = user.club.all()
            return render(request, 'club/myclublist.html', {"club_list": club_list})
        # get the club from the approval
        club = Club.objects.get(id=app.club_id)
        if not club:
            # if club does not exist, return error, redirect to myclublist page
            messages.error(request, "Club does not exist!")
            club_list = request.user.club.all()
            return render(request, 'club/myclublist.html', {"club_list": club_list})
        # get the pending user from the approval
        pending_user = User.objects.get(id=app.user_id)
        if not pending_user:
            # if the pending user does not exist, return error, redirect to manage club page
            messages.error(request, "Club does not exist!")
            approval_list = Approval.objects.filter(club=club, completed=0)
            return render(request, 'club/myclubmanage.html', {"approval_list": approval_list, "club": club})
        # get the approval from requst.POST
        approval = request.POST.get("approval")
        # Requires the current user to be the manager for approval
        if user == club.manager:
            # The decision to add a user to the club will be based on the approval,
            # and the approval will be marked as complete whether or not the approval is approved
            if approval == "approve":
                pending_user.club.add(club)
                app.completed = 1
                app.save()
            elif approval == "reject":
                app.completed = 1
                app.save()
            else:
                # if approval is not approve either reject, return error, redirect to manage club page
                messages.error(request, "Approval is not valid!")
                approval_list = Approval.objects.filter(club=club, completed=0)
                return render(request, 'club/myclubmanage.html', {"approval_list": approval_list, "club": club})
        else:
            # if the current user is not the manager, return error
            messages.error(request, 'you are not the manager')
        # get the latest approval list and return
        approval_list = Approval.objects.filter(club=club, completed=0)
        return render(request, 'club/myclubmanage.html', {"approval_list": approval_list, "club": club})


def contact(request):
    # show our contact
    return render(request, 'club/contact.html')


@login_required(login_url="/club/login")
def myclublist(request):
    # show myclubs function
    # Get all the clubs the current user belongs to and then return
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
    # user login function
    # if user already logged in, redirect to homepage
    if request.user.is_authenticated:
        return redirect('/club/')
    # If the request method is POST, try to pull out the relevant information.
    if request.method == 'POST':
        # create login form according to the form model
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # if login form is valid, get the user to log in
            user = login_form.cleaned_data['user']
            login(request, user)
            return redirect(reverse('club:index'))
    else:
        # If the request method is not POST, return an empty form
        login_form = LoginForm()
    return render(request, 'club/login.html', {'login_form': login_form})


def search(request):
    # search club function
    if request.method == 'POST':
        # get the search key
        key = request.POST.get("key")
        if not key:
            # if search key is none, return error, redirect to search page
            messages.error(request, "Search input is empty!")
            return render(request, 'club/search.html')
        # First search for names containing the key
        results = list(Club.objects.filter(name__icontains=key))
        if not results:
            # if none, search for types containing the key
            results = list(Club.objects.filter(type__icontains=key))
            if not results:
                # if still none, search for locations containing the key
                results = list(Club.objects.filter(location__icontains=key))
        return render(request, 'club/search.html', {"clubs": results})
    return render(request, 'club/search.html')


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('club:index'))


@login_required(login_url="/club/login")
def createClub(request):
    # create club function
    if request.user.is_authenticated:
        # Require authenticated users to access
        if request.method == "POST":
            club_form = CreateClubForm(request.POST)
            # create club form according to the form model
            if club_form.is_valid():
                # if club form is valid, save the form and Specify the manager as the current user
                club = club_form.save()
                club.manager = request.user
                club.save()
                user = request.user
                user.club.add(club)
                # redirect user to myclublist page
                return redirect('/club/myclublist')
        else:
            # If the request method is not POST, return an empty form
            club_form = CreateClubForm()
        return render(request, 'club/create_club.html', {'club_form': club_form})
    else:
        messages.error(request, 'Please log in first!')
        return redirect('/club/login')


@login_required(login_url="/club/login")
def viewClub(request, club_id):
    # view club function
    if request.user.is_authenticated:
        # Require authenticated users to access
        club = Club.objects.get(id=club_id)
        if not club:
            # if club does not exist, return error, redirect to myclublist page
            messages.error(request, "Club does not exist!")
            club_list = request.user.club.all()
            return render(request, 'club/myclublist.html', {"club_list": club_list})
        else:
            # get club members according to club_id, and return the members list and the club detail
            member_list = User.objects.filter(club=club)
            return render(request, 'club/clubdetails.html', {"member_list":member_list,"club":club})
    else:
        messages.error(request, 'Please log in first!')
        return redirect('/club/login')


@login_required(login_url="/club/login")
def joinClub(request):
    # join club function
    if request.user.is_authenticated:
        # Require authenticated users to access
        if request.method == "POST":
            club_id = request.POST.get("club_id")
            if not Club.objects.filter(id=club_id).first():
                # if club does not exist, return error, redirect to search page
                messages.error(request, "Club does not exist!")
                return render(request, 'club/search.html')
            # get current user
            user = request.user
            # only create new approval when this approval does not exist
            if not Approval.objects.get(user=user, club_id=club_id):
                # create an Approval model and save data
                approval = Approval(club_id=club_id, user=user)
                approval.save()
            return redirect("/club/")
    else:
        messages.error(request, 'Please log in first!')
        return redirect('/club/login')


@login_required(login_url="/club/login")
def removeMember(request):
    # remove member function
    if request.user.is_authenticated:
        if request.method == "POST":
            # get parameters form request.POST
            member_id = request.POST.get("member_id")
            club_id = request.POST.get("club_id")
            club = Club.objects.get(id=club_id)
            if not club:
                # if club does not exist, return error, redirect to myclublist page
                messages.error(request, "Club does not exist!")
                club_list = request.user.club.all()
                return render(request, 'club/myclublist.html', {"club_list": club_list})
            member = User.objects.get(id=member_id)
            if not member:
                # if member does not exist, return error, redirect to myclublist page
                messages.error(request, "Member does not exist!")
                member_list = User.objects.filter(club=club)
                return render(request, 'club/clubdetails.html', {"member_list": member_list, "club": club})
            if club not in member.club.all():
                # if member does not belong to this club, return error, redirect to club details page
                messages.error(request, "User "+member.username+"is not a member of the club!")
                member_list = User.objects.filter(club=club)
                return render(request, 'club/clubdetails.html', {"member_list": member_list, "club": club})
            # remove member frm the club
            member.club.remove(club)
            # get the new members list and return
            member_list = User.objects.filter(club=club)
            return render(request, 'club/clubdetails.html', {"member_list": member_list, "club": club})
    else:
        messages.error(request, 'Please log in first!')
        return redirect('/club/login')
