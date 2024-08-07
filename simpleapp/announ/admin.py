from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(Player)
admin.site.register(Announcement)
admin.site.register(Response)