from django.contrib import admin

from .models import ContenxtBox, IndexContent, MapsContent, NavbarFooter

# Register your models here.
class ContentBoxInline(admin.TabularInline):
    model = ContenxtBox

class IndexContentAdmin(admin.ModelAdmin):
    inlines = (ContentBoxInline,)

admin.site.register(IndexContent, IndexContentAdmin)
admin.site.register(ContenxtBox)
admin.site.register(MapsContent)
admin.site.register(NavbarFooter)
