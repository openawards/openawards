from django.contrib import admin

# Register your models here.
from django.apps import apps

admin.site.register(apps.get_model('openawards', 'User'))
admin.site.register(apps.get_model('openawards', 'Award'))
admin.site.register(apps.get_model('openawards', 'Work'))
admin.site.register(apps.get_model('openawards', 'License'))
