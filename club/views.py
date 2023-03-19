from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from club.models import User, Club, Approval, Comment
from club.forms import UserForm, searchClubForm
import json


def general_response(code, message="", data=[]):
    result = {"code": code, "message": message, "data": data}
    return HttpResponse(json.dumps(result))


def index(request):
    # request.session.set_test_cookie()
    context_dict = {}

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    response = render(request, 'club/index.html', context=context_dict)
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


def form(request):
    return render(request, 'club/form.html')


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
        user_form = UserForm(request.POST)

# If the two forms are valid...
        if user_form.is_valid():
        # Save the user's form data to the database.
            user = user_form.save()
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
            print(user_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        user_form = UserForm()

    # Render the template depending on the context.
    return render(request,
                'club/register.html',
                context = {'user_form': user_form, 'registered': registered})


def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
    # Gather the username and password provided by the user.
    # This information is obtained from the login form.
    # We use request.POST.get('<variable>') as opposed
    # to request.POST['<variable>'], because the
    # request.POST.get('<variable>') returns None if the
    # value does not exist, while request.POST['<variable>']
    # will raise a KeyError exception.
        email = request.POST.get('email')
        password = request.POST.get('password')
    # Use Django's machinery to attempt to see if the username/password
    # combination is valid - a User object is returned if it is.
        user = authenticate(email=email, password=password)
    # If we have a User object, the details are correct.
    # If None (Python's way of representing the absence of a value), no user
    # with matching credentials was found.
        if user:
    # Is the account active? It could have been disabled.
            if user.is_active:
    # If the account is valid and active, we can log the user in.
    # We'll send the user back to the homepage.
                login(request, user)
                request.session['email'] = email
                return redirect(reverse('club:index'))
            else:
    # An inactive account was used - no logging in!
                return HttpResponse("Your club account is disabled.")
        else:
    # Bad login details were provided. So we can't log the user in.
            print(f"Invalid login details: {email}, {password}")
            return HttpResponse("Invalid login details supplied.")
    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'club/login.html')


def search(request):
    #form = searchClubForm()
    #if request.method == 'POST':
        #print(form)
             #return index(request)
    #print(request.GET['location'])
    #a = request.GET['location']
    #results = Club.objects.filter(location=a)
    #data = [{'name': obj.name, 'type': obj.type, 'description': obj.description,'location':obj.location,'likes':obj.likes,'dislikes':obj.dislikes} for obj in results]
    #return JsonResponse({'data': data})
    #print(data)
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


def createClub(request):
    if request.method == "POST":
        user_id = request.session.get('user_id')
        name = request.POST.get("name")
        type = request.POST.get("type")
        location = request.POST.get("location")
        description = request.POST.get("description")

        if not user_id:
            message = "User is not logged in!"
            return general_response(400, message)
        if not User.objects.get(id=user_id):
            message = "User_id is invalid!"
            return general_response(400, message)
        if Club.objects.get(name=name):
            message = "CLube name has already been used"
            return general_response(400, message)

        club = Club(name=name, type=type, location=location, description=description, manager=user_id)
        club.save()
        return render(request, 'club/index.html', locals())


def viewClub(request):
    if request.method == "POST":
        user_id = request.session.get('user_id')
        club_id = request.POST.get("club_id")
        if not user_id:
            message = "User is not logged in!"
            return general_response(400, message)
        if not User.objects.get(id=user_id):
            message = "User_id is invalid!"
            return general_response(400, message)
        club = Club.objects.get(id=club_id)

        if not club:
            message = "CLube name has already been used"
            return general_response(400, message)
        else:
            data = {"name": club["name"], "type": club["type"], "location": club["location"],
                    "description": club["description"], "likes": club["likes"], "dislikes": club["dislikes"]}
        return render(request, 'club/myclub.html', locals())