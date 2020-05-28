import random
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import is_safe_url
from .models import Tweet
from .forms import TweetsForm

from .serializers import (TweetSerializer, TweetActionSerializer,TweetCreateSerializer)
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.
ALLOWED_HOSTS = settings.ALLOWED_HOSTS

def home_view(request, *args, **kwargs):
    
    return render(request, template_name='pages/home.html', context={}, status=200)

@api_view(["POST"]) #Http requests to this method
# @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args ,**kwargs):
    data =request.data or None        
    serializer = TweetCreateSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data,status=201)
    
    return Response({},status=400)


@api_view(["GET"])
def tweet_detail_view(request, tweet_id,*args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({},status=404)
    obj =qs.first()
    serializer = TweetSerializer(obj)
    
    return Response(serializer.data,status=200)

@api_view(["DELETE","POST"])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id,*args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({},status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message": "You cannot delete this tweet"},status=401)
    obj =qs.first()
    obj.delete()   
    return Response({"message": "Tweet has been deleted!"},status=200)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def tweet_action_view(request,*args, **kwargs):
    #id is required in the passed serialized data
    
    serializer = TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get("id")
        action = data.get("action")
        content = data.get("content")
        qs = Tweet.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({},status=404)        
        obj =qs.first() 

        if action == "like":
            obj.likes.add(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data,status=200)
        elif action == "unlike":            
            obj.likes.remove(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data,status=200)
        elif action == "retweet":             
            new_tweet = Tweet.objects.create(
                user=request.user,
                parent=obj,
                content =content) 
            serializer = TweetSerializer(new_tweet)
            return Response(serializer.data,status=201)
            pass
            
    return Response({},status=200)

@api_view(["GET"])
def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()    
    username = request.GET.get('username')
    print(username)
    if username != None:
        qs = qs.filter(user__username__iexact=username)
    
    serializer = TweetSerializer(qs, many=True)
    
    return Response(serializer.data)


def  tweet_create_view_pure_django(request, *args,**kwargs):
    #Get user from the request
    user =request.user    
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({},status=401)
        return redirect(settings.LOGIN_URL)  
    #print("ajax",request.is_ajax())
    #Get the form data from the request object
    form =TweetsForm(request.POST or None)    
    #Get the value attribute from the input element in the form
    next_url = request.POST.get('next') or None    
    #Save the data in the database if they are valid
    if form.is_valid():
        obj = form.save(commit=False)        
        obj.user = user
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(),status=201)
        #if next_url != None and is_safe_url(next_url,ALLOWED_HOSTS):
        #    return redirect(next_url) 
        #Rest the form
        form = TweetsForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors,status=400)
    return render(request, 'components/form.html' ,context ={"form": form})




def tweet_list_view_pure_django(request, *args, **kwargs):
    query = Tweet.objects.all()
    tweet_list = [x.serialize() for x in query]
    data = {
        'isUser':False,
        'response': tweet_list
    }

    return JsonResponse(data)


def tweet_detail_view_pure_django(request, tweet_id, *args, **kwargs):
    data = {
        "id": tweet_id,
    }
    status = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content

    except:
        data['message'] = 'Notfound'
        status = 404

    return JsonResponse(data, status=status)
