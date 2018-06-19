from django.contrib import admin
from .models import Store,  Coupon, Category, CouponType, Deal
from mptt.admin import MPTTModelAdmin


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

class CategoryAdmin(MPTTModelAdmin):
    fields = ['name', 'parent']
    list_display = ('name',)

    mptt_level_indent = 15
#class CategoryAdmin(admin.ModelAdmin):
    #list_display = ('name', 'slug',)
   # search_fields = ('name',)

    #prepopulated_fields = {'slug': ('name',)}


class DealAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'old_price', 'categoryId', 'shop')
    search_fields = ('name',)
    readonly_fields = ('slug',)
    list_editable = ['price', 'old_price', 'categoryId']
    list_filter = ('categoryId',)


admin.site.register(Deal, DealAdmin)
admin.site.register(Store, StoreAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(CouponType, CouponTypeAdmin)
admin.site.register(Category, CategoryAdmin)




