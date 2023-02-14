from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView

from .models import Tag, Quote, Author
from .forms import QuoteForm, AuthorForm


class AboutAuthorView(DetailView):
    model = Author
    template_name = 'quote/about_author.html'
    context_object_name = 'author'


def main(request):
    quotes = Quote.objects.all()
    context = {'quotes': quotes}
    return render(request, 'quoteapp/index.html', context)


def author(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'quoteapp/author_detail.html', {'author': author})


@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.username = request.user.username
            quote.save()
            return redirect(to='quoteapp:main')
        else:
            form = QuoteForm()
        return render(request, 'quoteapp/add_quote.html', {'form': form})

    return render(request, 'quoteapp/add_quote.html', {'form': QuoteForm()})
    # if request.method == 'POST':
    #     print(request.POST.keys())
    #     quote_text = request.POST.get('quote_text', '')
    #     author_name = request.POST.get('author_name', '')
    #     tags = request.POST.getlist('tags')
    #
    #     author, created = Author.objects.get_or_create(
    #         fullname = author_name
    #     )
    #
    #     existing_quote = Quote.objects.filter(quote = quote_text).first()
    #     if existing_quote:
    #         quote = existing_quote
    #     else:
    #         quote = Quote.objects.create(
    #             quote = quote_text,
    #             author = author
    #         )
    #
    #     for tag_name in tags :
    #         tag, created = Tag.objects.get_or_create(
    #             name = tag_name
    #         )
    #         quote.tags.add(tag)
    # return render(request, 'quoteapp/add_quote.html')


    # tags = Tag.objects.all()
    # if request.method == 'POST':
    #     form = QuoteForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('quoteapp:main')
    # # if request.method == 'POST':
    # #     form = QuoteForm(request.POST)
    # #     # if form.is_valid():
    # #     author_name = form.cleaned_data.get('fullname')
    # #     author, created = Author.objects.get_or_create(name = author_name)
    # #     print(f'{author=}')
    # #
    # #     quote = form.save(commit = False)
    # #     print(f'{author=}')
    # #     quote.author = author
    # #     quote.save()
    # #     form.save_m2m()
    # #     return redirect('quoteapp:index')
    # else:
    #     form = QuoteForm()
    # return render(request, 'quoteapp/add_quote.html', {'form': form})

    # if request.method == 'POST':
    #     form = QuoteForm(request.POST)
    #     if form.is_valid():
    #         quote_text = form.cleaned_data['quote']
    #         author_name = form.cleaned_data['author']
    #
    #         try:
    #             author = Author.objects.get(name=author_name)
    #         except Author.DoesNotExist:
    #             author = Author.objects.create(name=author_name)
    #
    #         quote = Quote.objects.create(quote=quote_text, author=author)
    #         quote.tags.set(tags)
    #
    #         return redirect('quoteapp:main')
    # else:
    #     form = QuoteForm()
    #
    # return render(request, 'quoteapp/add_quote.html', {'form': form})

    # if request.method == 'POST':
    #     form = QuoteForm(request.POST)
    #     if form.is_valid():
    #         quote = form.save()
    #         tags = form.cleaned_data['tags']
    #
    #     for tag in tags.split(',') :
    #         Tag.objects.get_or_create(name = tag)
    #         quote.tags.add(Tag.objects.get(name = tag))
    #     quote.save()
    #     return redirect('quoteapp:quotes')
    # else:
    #     form = QuoteForm()

        #     new_quote = form.save()
        #
        #     choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
        #     for tag in choice_tags.iterator():
        #         new_quote.tags.add(tag)
        #
        #     return redirect(to='quoteapp:main')
        # else:
        # return render(request, 'quoteapp/add_quote.html', {"tags": tags, 'form': form})

    # return render(request, 'quoteapp/add_quote.html', {"tags": tags, 'form': QuoteForm()})


@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quoteapp:main')
        else:
            form = AuthorForm()
        return render(request, 'quoteapp/add_author.html', {'form': form})

    return render(request, 'quoteapp/add_author.html', {'form': AuthorForm})


