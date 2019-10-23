from django.contrib import admin
from .models import Catagory, TV, Episode, Season

# Register your models here.


class TvAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'catagory', 'views', 'date')
    list_filter = ('year', 'catagory')
    search_fields = ('title', 'year', 'catagory')
    list_per_page = 30


class TvCatAdmin (admin.ModelAdmin):
    list_display = ('name', 'date')
    list_per_page = 30


admin.site.register(TV, TvAdmin)
admin.site.register(Catagory, TvCatAdmin)
admin.site.register(Season)
admin.site.register(Episode)
