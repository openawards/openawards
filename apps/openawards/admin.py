from django.contrib import admin
from openawards.models import User, License, Work, Award, Vote, Coupon, CouponCampaign


class CouponAdmin(admin.ModelAdmin):
    list_display = ('date_created', 'campaign', 'user', 'code', 'price', 'exchanged')
    list_filter = ('campaign', 'date_created', ('user', admin.RelatedOnlyFieldListFilter), 'exchanged',
                   'date_exchanged')
    search_fields = ('code', 'price', 'user__first_name', 'user__email')


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'remain_credits',)


class VoteAdmin(admin.ModelAdmin):
    list_display = ('voted_on', 'fan', 'award', 'work',)


admin.site.register(User, UserAdmin)
admin.site.register(License)
admin.site.register(Work)
admin.site.register(Award)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(CouponCampaign)

# To have it at the beginning for testing purposes:
admin.site.register(Vote, VoteAdmin)
