from django.contrib import admin

from .models import *


class ImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'description', 'slug', 'photo')
    prepopulated_fields = {"slug": ("description",)}
    fields = ('user', 'photo', 'description', 'slug')
    save_on_top = True


admin.site.register(Images, ImagesAdmin)
