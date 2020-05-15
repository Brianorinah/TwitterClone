from django.db import models
import random
from django.conf import settings

# Create your models here.
user = settings.AUTH_USER_MODEL

class Tweet(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)

    #def __str__(self):
    #    return self.content


    #Enabling last tweet to be viewed first
    class Meta:
        ordering =['-id']

    #Method to return a dictionary of tweet data
    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0,255)
        }
