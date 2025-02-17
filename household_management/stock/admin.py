from django.contrib import admin

# Register your models here.
from .models import Stock

admin.site.register(Stock)  # ✅ Now the Stock model is visible in the admin panel