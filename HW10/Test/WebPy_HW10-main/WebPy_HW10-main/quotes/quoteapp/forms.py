from django.forms import ModelForm, CharField, TextInput, DateField
from django import forms
from .models import Author, Quote, Tag


class QuoteForm(ModelForm):
    quote = CharField(max_length=2500, required=True, widget=TextInput())
    tags = forms.CharField(required = True)

    class Meta:
        model = Quote
        fields = ['quote', 'author']
        # exclude = ['tags']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].queryset = Author.objects.all()
        self.fields['tags'] = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())


class AuthorForm(ModelForm):
    fullname = CharField(max_length=100, required=True, widget=TextInput())
    born_date = DateField(required=True, input_formats=['%Y-%m-%d', '%m/%d/%Y'])
    born_location = CharField(max_length=100, required=True, widget=TextInput())
    description = CharField(max_length=5000, required=True, widget=TextInput())

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']
        exclude = ['tags']