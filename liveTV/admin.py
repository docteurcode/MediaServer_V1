from django.contrib import admin
from .models import Catagory, Channel

# Register your models here.


class ChannelAdmin(admin.ModelAdmin):
    list_display = ('name',  'popular', 'date')
    list_filter = ('caragory',)
    search_fields = ('name', 'overview', 'link_1', 'link_2')
    list_per_page = 20


class CatagoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')
    list_per_page = 20


admin.site.register(Channel, ChannelAdmin)
admin.site.register(Catagory)
