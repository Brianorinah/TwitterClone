import random
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import is_safe_url

# Create your views here.
ALLOWED_HOSTS = settings.ALLOWED_HOSTS

def home_view(request, *args, **kwargs):
    username = None
    if request.user.is_authenticated:
        username = request.user.username    
    return render(request, template_name='pages/home.html', context={"username"}, status=200)

def tweets_list_view(request, *args, **kwargs):

   # print("tlv:",request.data)
    print("tlv user:",request.user)
      
    return render(request, template_name='tweets/list.html')

def tweets_detail_view(request,tweet_id, *args, **kwargs):    
       
    return render(request, template_name='tweets/detail.html', context={"tweet_id":tweet_id})

def tweets_profile_view(request, username, *args, **kwargs):    
      
    return render(request, template_name='tweets/profile.html', context={"profile_username": username}, status=200)

