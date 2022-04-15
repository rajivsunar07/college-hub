from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
from group.models import Group
import math
# Create your models here.

type_choices = (('post','post'),('news','news'),('poll','poll'),('invite','invite'))
verification_choices = (('accepted','accepted'),('declined','declied'),('pending','pending'))
class Post(models.Model):
    content = models.TextField()
    image = models.FileField(null=True, blank=True, upload_to='post_pics')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # for verification in home page
    verification = models.CharField(default='accepted', choices=verification_choices, max_length=150)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=150,choices=type_choices, default='post')


    # returns the date_posted in seconds, days, months or years
    def published(self):
        time_diff= timezone.now() - self.date_posted
        time = 0
        return_stmt = ""

        if time_diff.days == 0:
            if time_diff.seconds >= 0 and time_diff.seconds < 60:
                time = time_diff.seconds
                return_stmt = str(time) + " second"
            elif time_diff.seconds >= 60 and time_diff.seconds < 3600:
                time = math.floor(time_diff.seconds/60)
                return_stmt = str(time) + " minute"
            elif time_diff.seconds >= 3600 and time_diff.seconds < 86400:
                time = math.floor(time_diff.seconds/3600)
                return_stmt = str(time) + " hour"
        # 1 day to 30 days
        elif time_diff.days >= 1:
            if time_diff.days < 30:
                time = time_diff.days
                return_stmt = str(time) + " day"     
            elif time_diff.days >= 30 and time_diff.days < 365:
                time = math.floor(time_diff.days/30) 
                return_stmt = str(time) + " month"          
            elif time_diff.days >= 365:
                time = math.floor(time_diff.days/365)
                return_stmt = str(time) + " year"
            

        if time == 1:
            return return_stmt
        return return_stmt + "s"



    class Meta:
        db_table = "Post"
        ordering = ["-date_posted"]

    
class Comments(models.Model):
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        db_table = "Comments"
        ordering = ["-date_posted"]

# options in a poll or invite
class PostOption(models.Model):
    option = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    clicked_value = models.IntegerField(default=0)
    clicked_percent = models.IntegerField(default=0)

    def __str__(self):
        return self.option
    
    class Meta:
        db_table = "PostOption"

# options clicked by a user
class ClickedPost(models.Model):
    option = models.ForeignKey(PostOption, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.option.option
    
    class Meta:
        db_table = "ClickedPost"
