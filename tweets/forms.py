from django import forms
from django.conf import settings


from .views import Tweet

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH

class TweetsForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']
     
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content)> MAX_TWEET_LENGTH:
            raise forms.ValidationError("Tweet too long")        
        return content