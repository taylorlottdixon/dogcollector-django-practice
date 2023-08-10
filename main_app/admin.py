from django.contrib import admin
from .models import Dog, Feeding, Walk, Photo
# Register your models here.
admin.site.register(Dog)
admin.site.register(Feeding)
admin.site.register(Walk)
admin.site.register(Photo)