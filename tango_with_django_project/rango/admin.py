from django.contrib import admin
from rango.models import Category, Page


#class ChoiceInline(admin.StackedInline):
#    model = Page
#    extra = 3

class PageAdmin(admin.ModelAdmin):
    fields = ['category', 'title']
#    inlines = [ChoiceInline]
    list_display = ('title', 'category', 'url')
	

admin.site.register(Category)
admin.site.register(Page, PageAdmin)