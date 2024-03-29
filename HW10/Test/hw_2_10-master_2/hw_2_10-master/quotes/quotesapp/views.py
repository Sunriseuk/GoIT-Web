from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .forms import TagForm, AuthorForm, QuoteForm
from .models import Tag, Author, Quote


# Create your views here.


def reformat_author_name(name):
    return name.replace(' ', '-')


def main(request):
    quotes = Quote.objects.all()
    authors = Author.objects.all()
    tags = Tag.objects.all()


    paginator = Paginator(quotes, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "quotesapp/index.html",
                  context={"authors": authors, "quotes": quotes, "tags": tags, "page_obj": page_obj})


@login_required
def addtag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotesapp:main')
        else:
            return render(request, 'quotesapp/addtag.html', {'form': form})

    return render(request, 'quotesapp/addtag.html', {'form': TagForm()})


@login_required
def addauthor(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotesapp:main')
        else:
            return render(request, 'quotesapp/addauthor.html', {'form': form})

    return render(request, 'quotesapp/addauthor.html', {'form': AuthorForm()})


@login_required
def addqoute(request):
    tags = Tag.objects.all()
    authors = Author.objects.all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)

                return redirect(to='quotesapp:main')
        else:
            return render(request, 'quotesapp/addquote.html', {"tags": tags, "authors": authors, 'form': form})

    return render(request, 'quotesapp/addquote.html', {"tags": tags, "authors": authors, 'form': QuoteForm()})


class AuthorPage(View):
    template_name = "noteapp/author.html"

    def get(self, request, fullname):
        author = get_object_or_404(Author, full_name=fullname)
        return render(request, self.template_name, {"author": author})
