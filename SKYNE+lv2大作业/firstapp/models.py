from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=500)
    img = models.CharField(null=True, blank=True, max_length=250)
    content = models.TextField(null=True, blank=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    createtime = models.DateField()
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    name = models.CharField(max_length=500)
    avatar = models.CharField(max_length=250, default="static/images/default.png")
    comment = models.TextField(null=True, blank=True)
    createtime = models.DateField(auto_now=True)

    belong_to = models.ForeignKey(to=Article, related_name="under_comments", null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Ticket(models.Model):
    voter = models.ForeignKey(to=User, related_name="user_tickets", on_delete=models.CASCADE)
    article = models.ForeignKey(to=Article, related_name="article_tickets", on_delete=models.CASCADE)

    ARTICLE_CHOICES = {
        ("like", "like"),
        ("dislike", "dislike"),
        ("normal", "normal")
    }
    choice = models.CharField(choices=ARTICLE_CHOICES, max_length=10)

    def __str__(self):
        return str(self.id)

class UserProfile(models.Model):
    belong_to = models.OneToOneField(to= User, null=True, related_name='belong_to', on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to= 'cover_img', null= True)
    choices = {
        ("male", "男"),
        ("female", "女"),
    }
    sex = models.CharField(null= False, max_length= 5, choices= choices, default='male')

