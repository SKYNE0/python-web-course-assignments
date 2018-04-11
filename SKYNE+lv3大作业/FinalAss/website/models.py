from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    belong_to = models.OneToOneField(to=User, related_name='profile')
    profile_image = models.FileField(upload_to='profile_image')
    ROLE_CHOICES = (
        ('normal', 'normal'),
        ('author', 'author'),
        )
    role = models.CharField(choices=ROLE_CHOICES, max_length=10, default="normal")

    def __str__(self):
        return "id:{},belong_to.username:{}".format(self.id,self.belong_to.username)


class Video(models.Model):
    title = models.CharField(null=True, blank=True, max_length=300)
    content = models.TextField(null=True, blank=True)
    url_image = models.URLField(null=True, blank=True)
    cover = models.FileField(upload_to='cover_image', null=True)
    editors_choice = models.BooleanField(default=False)
    owner = models.ForeignKey(to=UserProfile, related_name='videos', default=1)

    def __str__(self):
        return "Title:{},user-username:{}".format(self.title,self.owner.belong_to.username)


class Ticket(models.Model):
    voter = models.ForeignKey(to=UserProfile, related_name='voted_tickets')
    video = models.ForeignKey(to=Video, related_name='tickets')
    VOTE_CHOICES = (
        ('like', 'like'),
        ('dislike', 'dislike'),
        ('normal', 'normal'),
        )
    choice = models.CharField(choices=VOTE_CHOICES, max_length=10)

    def __str__(self):
        return str(self.id)
