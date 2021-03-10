from django.contrib import admin
from .models import User, Dog, City
# Register your models here.

admin.site.register(User)
admin.site.register(Dog)
admin.site.register(City)
