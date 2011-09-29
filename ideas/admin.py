from django.contrib import admin
from i2.ideas.models import UserProfile, Idea, Message

admin.site.register(UserProfile)
admin.site.register(Message)
admin.site.register(Idea)
