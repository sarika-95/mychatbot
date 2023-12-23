from django.contrib import admin

# Register your models here.
# myapi/admin.py

from .models import Item

admin.site.register(Item)
