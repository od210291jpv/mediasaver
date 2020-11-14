from django.contrib import admin
from .models import ImageFile, UserAccount, Category

# Register your models here.
admin.site.register(ImageFile)
admin.site.register(UserAccount)
admin.site.register(Category)

