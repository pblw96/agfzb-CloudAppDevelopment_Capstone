from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel, CarDealer, DealerReview
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request, get_dealer_by_id
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {'nbar': 'about'}
    if request.method == 'GET':
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {'nbar': 'contact'}
    if request.method == 'GET':
        return render(request, 'djangoapp/contact.html', context)


# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('psw')
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            logger.error('Wrong username or password')
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html' , context)
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('psw')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        user_exist = False
        try:
            User.objects.get(username = username)
            user_exist = True
        except:
            logger.error('new user')
        
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {'nbar':'index'}
    if request.method == "GET":
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/p.congiu96%40gmail.com_dev/dealership-package/get-dealerships"
        dealerships = get_dealers_from_cf(url)
        context['dealerships'] = dealerships
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id, dealer_name):
    context = {}
    if request.method == 'GET':
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/p.congiu96%40gmail.com_dev/dealership-package/get-review"
        dealer_reviews = get_dealer_reviews_from_cf(url, dealer_id = dealer_id)
        context['reviews'] = dealer_reviews
        context['dealer_name'] = dealer_name
        context['dealer_id'] = dealer_id
        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    cars = CarModel.objects.filter(dealer_id=dealer_id)
    dealer = get_dealer_by_id(url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/p.congiu96%40gmail.com_dev/dealership-package/get-dealerships",
                              dealer_id = dealer_id)
    
    if request.method == 'GET':
        context = {}
        try:

            context['dealer'] = dealer
            context['dealer_id'] = dealer.id
            context['cars'] = cars
        except:
            logger.error('Dealer not found')
        return render(request, 'djangoapp/add_review.html', context)
    
    if User.is_authenticated and request.method == 'POST':
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/p.congiu96%40gmail.com_dev/dealership-package/post-review"
        review = {}
        json_payload = {}

        car = cars.get(id = request.POST['car'])
        purchase_check = request.POST.get('purchasecheck', 'off')

        review['id'] = request.user.id
        review['name'] = request.user.get_full_name()
        review['dealership'] = dealer_id
        review['review'] = request.POST["content"]
        review['purchase'] = True if purchase_check == 'on' else False
        review['purchase_date'] = request.POST['purchasedate']
        review['car_make'] = str(car.car_make)
        review['car_model'] = str(car.name)
        review['car_year'] = car.year.strftime("%Y")

        json_payload["review"] = review

        post_request(url, json_payload)

        return redirect('djangoapp:dealer_details', dealer_id, dealer.full_name)


        
