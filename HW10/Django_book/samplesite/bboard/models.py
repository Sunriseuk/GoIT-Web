from django.db import models


# Фнешний вид Админки
class Bb (models.Model):
    title = models.CharField(max_length=50, verbose_name='Товар')
    content = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(null=True, blank=True, verbose_name='Цена')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    rubric = models.ForeignKey('Rubric', null=True, on_delete=models.PROTECT, verbose_name='Рубрика')

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        ordering = ['-published']


class Rubric (models.Model) :
    name = models. CharField (max_length=20, db_index=True, verbose_name='Название')
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['name']



# class Bb(models.Model):
#     objects = None
#     title = models.CharField(
#         max_length=50)  # заголовок объявления с названием продаваемого товара (тип — строковый, длина — 50 символов)
#     content = models.TextField(null=True, blank=True)  # сам текст объявления, описание товара
#     price = models.FloatField(null=True, blank=True)  # цена (тип — вещественное число)
#     published = models.DateTimeField(auto_now_add=True, db_index=True)  # дата публикации

'''CharField — обычное строковое поле фиксированной длины. Допустимая длина
значения указывается параметром max length конструктора;
 TextField— текстовое поле неограниченной длины, или memo-поле. Присвоив
параметрам null и blank конструктора значения True, мы укажем, что это поле
можно не заполнять (по умолчанию любое поле обязательно к заполнению);
 FloatField— поле для хранения вещественных чисел. Оно также необязательно
для заполнения (см. параметры его конструктора);
 DateTimeField— поле для хранения временной отметки. Присвоив параметру
auto now add конструктора значение True, мы предпишем Django при создании
новой записи заносить в это поле текущие дату и время. А параметр db index
при присваивании ему значения True укажет создать для этого поля индекс (при
выводе объявлений мы будем сортировать их по убыванию даты публикации,
и индекс здесь очень пригодится).

В классе модели мы объявили вложенный класс Meta, а в нем — атрибуты класса,
которые зададут параметры уже самой модели:
□ verbose name piurai — название модели во множественном числе;
□ verbose name — название модели в единственном числе.
Эти названия также будут выводиться на экран;
□ ordering — последовательность


Класс ForeignKey представляет поле внешнего ключа, в котором фактически будет
храниться ключ записи из первичной модели. Первым параметром конструктору
этого класса передается строка с именем класса первичной модели, поскольку вторичная
модель у нас объявлена раньше первичной.
Все поля моделей по умолчанию обязательны к заполнению. Следовательно, добавить
новое, обязательное к заполнению поле в модель, которая уже содержит записи,
нельзя — сама СУБД откажется делать это и выведет сообщение об ошибке.
Нам придется явно пометить добавляемое поле rubric как необязательное, присвоив
параметру null значение True.
Именованный параметр on deiete управляет каскадными удалениями записей вторичной
модели после удаления записи первичной модели, с которой они были связаны.
Значение protect этого параметра запрещает каскадные удаления (чтобы
какой-нибудь несообразительный администратор не стер разом уйму объявлений,
удалив рубрику, к которой они относятся).

'''