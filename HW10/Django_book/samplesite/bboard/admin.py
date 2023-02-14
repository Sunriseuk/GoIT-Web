from django.contrib import admin

# Разделы, которые будут видны в админке.
from .models import Bb
from .models import Rubric

class BbAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'price', 'published', 'rubric')
    list_display_links = ('title', 'content')
    search_fields = ('title', 'content',)

admin.site.register(Bb, BbAdmin)
admin.site.register(Rubric)


'''
Класс редактора объявляется как производный от класса ModelAdmin из модуля
django. cont rib. admin. Он содержит набор атрибутов класса, которые и задают параметры
представления модели. Мы использовали следующие атрибуты класса:
□ list display— последовательность имен полей, которые должны выводиться
в списке записей;
□ list—dispiay_links— последовательность имен полей, которые должны быть
преобразованы в гиперссылки, ведущие на страницу правки записи;
□ search—fields— последовательность имен полей, по которым должна выполняться
фильтрация.




'''