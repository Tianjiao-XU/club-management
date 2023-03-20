from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from club.models import User, Club, Approval, Comment
from club.forms import RegisterForm, LoginForm, CreateClubForm
import json


def general_response(code, message="", data=[]):
    result = {"code": code, "message": message, "data": data}
    return HttpResponse(json.dumps(result))


def index(request):
    # request.session.set_test_cookie()
    # visitor_cookie_handler(request)
    # context_dict['visits'] = request.session['visits']
    club_list  = Club.objects.order_by('-likes')[:3]
    context_dict = {'club_list':club_list}
    response = render(request, 'club/index.html', context_dict)
    return response


def myClub(request):
    # if request.session.test_cookie_worked():
    #     print("TEST COOKIE WORKED!")
    #     request.session.delete_test_cookie()
    return render(request, 'club/myclub.html')

def myclubevaluate(request):
    return render(request, 'club/myclubevaluate.html')


def myclubmanage(request):
    return render(request, 'club/myclubmanage.html')


def contact(request):
    return render(request, 'club/contact.html')


def register(request):
# A boolean value for telling the template
# whether the registration was successful.
# Set to False initially. Code changes value to
# True when registration succeeds.
    registered = False

# If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
# Attempt to grab information from the raw form information.
# Note that we make use of both UserForm and UserProfileForm.
        register_form = RegisterForm(request.POST)

# If the two forms are valid...
        if register_form.is_valid():
        # Save the user's form data to the database.
            user = register_form.save()
         # Now we hash the password with the set_password method.
         # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Update our variable to indicate that the template
            # registration was successful.
            registered = True
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(register_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        register_form = RegisterForm()

    # Render the template depending on the context.
    return render(request,
                'club/register.html',
                context = {'register_form': register_form, 'registered': registered})


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
        if request.POST.get('type'):
            print(request.POST['type'])
            a = request.POST['type']
            results = Club.objects.filter(type=a)
        else:
            print(request.POST['location'])
            a = request.POST['location']
            results = Club.objects.filter(location=a)
        clubs = [{'name': obj.name, 'type': obj.type, 'description': obj.description,'location':obj.location,'likes':obj.likes,'dislikes':obj.dislikes} for obj in results]
        print(clubs)
        return render(request,'club/search.html', {"clubs":clubs})
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


@login_required(login_url='/club/login')
def createClub(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            club_form = CreateClubForm(request.POST)
            if club_form.is_valid():
                club_form.save(commit=True)
                return redirect('/club/')
        else:
            club_form = CreateClubForm()
        return render(request, 'club/create_club.html', {'club_form': club_form})
    else:
        messages.error(request, 'Please log in first!')
        return redirect('/club/login')


@login_required(login_url='/club/login')
def viewClub(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            club_id = request.POST.get("club_id")
            club = Club.objects.get(id=club_id)

            if not club:
                message = "CLube name has already been used"
                return general_response(400, message)
            else:
                data = {"name": club["name"], "type": club["type"], "location": club["location"],
                        "description": club["description"], "likes": club["likes"], "dislikes": club["dislikes"]}
            return render(request, 'club/myclub.html', locals())
    else:
        messages.error(request, 'Please log in first!')
        return redirect('/club/login')