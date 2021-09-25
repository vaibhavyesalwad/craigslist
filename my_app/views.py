import requests
import re
from django.shortcuts import render
from bs4 import BeautifulSoup
from . import models
from requests.compat import quote_plus

# Create your views here.

BASE_CRAIGSLIST_URL = "https://hyderabad.craigslist.org/d/services/search/?query={}"


def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response_search = requests.get(final_url)

    print(final_url)

    soup = BeautifulSoup(response_search.text, features="html.parser")
    post_listings = soup.find_all("li", attrs={'class': 'result-row'})

    final_postings = []
    for post in post_listings:
        current_post = post.find("a", {'class': 'result-title'})
        post_title = current_post.text
        post_url = current_post['href']
        post_location_class = post.find("span", {'class': 'result-hood'})

        if post_location_class:
            post_location = post_location_class.text
        else:
            post_location = post.find("span", {'class': 'nearby'}).text

        post_price_class = post.find("span", {'class': 'result-price'})

        if post_price_class:
            post_price = post_price_class.text
        else:
            post_price = None

        post_location = re.sub('[()]', '', post_location)
        # post_location = post_location.split()[-1]

        response_post = requests.get(post_url)

        post_soup = BeautifulSoup(response_post.text, 'html.parser')

        post_image = post_soup.find("div", {'class': 'slide first visible'})

        if post_image:
            post_image_url = post_image.find("img")['src']
        else:
            post_image_url = None

        final_postings.append(
            (post_title, post_url, post_location, post_image_url, post_price))

    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)
