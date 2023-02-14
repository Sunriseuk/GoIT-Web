from django.contrib import admin
from .models import Author, Quote, Tag
# Register your models here.


class QuotesAdmin(admin.ModelAdmin):
    list_filter = ("author", "text")
    list_display = ("text", "author")


admin.site.register(Author)
admin.site.register(Quote, QuotesAdmin)
admin.site.register(Tag)