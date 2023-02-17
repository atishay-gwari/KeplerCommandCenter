from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Upload)
admin.site.register(Csv)
admin.site.register(CovertedToDB)