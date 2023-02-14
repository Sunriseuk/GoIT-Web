from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .models import Bb, Rubric
from .forms import BbForm


def index(request):
    bbs = Bb.objects.all()
    rubrics = Rubric.objects.all()
    context = {'bbs': bbs, 'rubrics': rubrics}
    return render(request, 'bboard/index.html', context)

def by_rubric(request, rubric_id):
    bbs = Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.all()
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}
    return render(request, 'bboard/by_rubric.html', context)


class BbCreateView(CreateView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    success_url = reverse_lazy('index')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

# def index(request):
#     s = 'Список объявлений\r\n\r\n\r\n'
#     for bb in Bb.objects.order_by('-published'): #order_by - отсортировать объявления по убыванию даты их публикации
#         s += bb.title + '\r\n' + bb.content + '\r\n\r\n'
#     return HttpResponse(s, content_type='text/plain; charset=utf-8')
#отправляет клиенту текстовое сообщение: Здесь будет выведен список объявлений.

'''Любой контроллер-функция в качестве единственного обязательного параметра
принимает экземпляр класса HttpRequest, хранящий различные сведения о полученном
запросе: запрашиваемый интернет-адрес, данные, полученные от посетителя,
служебную информацию от самого веб-обозревателя и пр. По традиции этот
параметр называется request. В нашем случае мы его никак не используем.

В теле функции мы создаем экземпляр класса HttpResponse (он объявлен в модуле
django.http), который будет представлять ответ, отправляемый клиенту. Содержимое
этого ответа — собственно текстовое сообщение — указываем единственным
параметром конструктора этого класса. Готовый экземпляр класса возвращаем
в качестве результата.

Контроллер-класс мы сделали производным от класса createview из модуля
django.views.generic.edit. Базовый класс "знает", как создать форму, вывести на
экран страницу с применением указанного шаблона, получить занесенные в форму
данные, проверить их, сохранить в новой записи модели и перенаправить пользователя
в случае успеха на заданный интернет-адрес.
Все необходимые сведения мы указали в атрибутах объявленного класса:
□ tempiate name — путь к файлу шаблона, создающего страницу с формой;
□ form ciass — ссылка на класс формы, связанной с моделью;
□ success_url — интернет-адрес для перенаправления после успешного сохранения
данных (в нашем случае это адрес главной страницы).


'''