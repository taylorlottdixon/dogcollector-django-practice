from django.contrib import admin
from .models import Dog, Feeding, Walk
# Register your models here.
admin.site.register(Dog)
admin.site.register(Feeding)
admin.site.register(Walk)
