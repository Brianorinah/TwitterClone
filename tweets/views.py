import random
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import is_safe_url
from .models import Tweet
from .forms import TweetsForm

# Create your views here.
ALLOWED_HOSTS = settings.ALLOWED_HOSTS

def home_view(request, *args, **kwargs):
    
    return render(request, template_name='pages/home.html', context={}, status=200)

def  tweet_create_view(request, *args,**kwargs):
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




def tweet_list_view(request, *args, **kwargs):
    query = Tweet.objects.all()
    tweet_list = [x.serialize() for x in query]
    data = {
        'isUser':False,
        'response': tweet_list
    }

    return JsonResponse(data)


def tweet_detail_view(request, tweet_id, *args, **kwargs):
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
