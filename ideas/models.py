from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
#from i2.ideas import views

class UserMethods:
    def name(self):
        return self.first_name + " " + self.last_name

User.__bases__ += (UserMethods,)

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    fbid = models.BigIntegerField(default=0, primary_key=True)
#    friends = models.ManyToManyField("self")
    access_token = models.CharField(max_length=200, default='')

    def get_friends(self):
        return self.friends.all()

    def __unicode__(self):
        return "%s" % self.user

class Idea(models.Model):
    author = models.ForeignKey(User, related_name="author_idea")
    ideaname = models.CharField(max_length=30)
    ideadescription = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s created %s at %s" % (self.author, self.ideaname, self.created_at)

class IdeaForm(ModelForm):
    class Meta:
        model = Idea
        fields = ('ideaname', 'ideadescription')

class IdeaSubmitForm(forms.Form):
#    ideaname = models.CharField(max_length=30, label='Title')
#    ideadescription = models.CharField(max_length=200, label='Description')
#
    class Meta:
        model = Idea
        fields = ('ideaname', 'ideadescription')

# Create your models here.
