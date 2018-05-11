from django.contrib import admin
from .models import Store,  Coupon, Category, CouponType


class StoreAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug',)
    search_fields = ('title',)
    readonly_fields = ('slug',)


class CouponAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)
    list_display = ('title', 'slug', 'promocode', 'expired')
    list_editable = ['expired']


class CouponTypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'slug',)
    search_fields = ('type',)

    prepopulated_fields = {'slug': ('type',)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    search_fields = ('name',)

    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Store, StoreAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(CouponType, CouponTypeAdmin)
admin.site.register(Category, CategoryAdmin)
