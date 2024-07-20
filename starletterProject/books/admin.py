from django.contrib import admin
from .models import *

admin.site.register(Book)
admin.site.register(Page)
admin.site.register(PageImage)
admin.site.register(Note)