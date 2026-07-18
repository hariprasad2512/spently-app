from django.contrib import admin
from .models import Category, Transaction
# Both these are visible to the SuperUser

admin.site.register(Category)
admin.site.register(Transaction)