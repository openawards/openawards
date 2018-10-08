from django.contrib import admin

# Register your models here.

from openawards.models import User, License, Work, Award, Vote

admin.site.register(User)
admin.site.register(License)
admin.site.register(Work)
admin.site.register(Award)
# To have it at the beginning for testing purposes:
admin.site.register(Vote)