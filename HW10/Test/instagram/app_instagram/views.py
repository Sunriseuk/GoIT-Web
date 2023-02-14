import os

from django.conf import settings
from django.shortcuts import render, redirect

from .forms import PictureForm
from .models import Picture
# Create your views here.


def main(request):
    return render(request, "app_instagram/index.html", context={"title": "Killer Instagram"})


def upload(request):
    form = PictureForm(instance=Picture())
    if request.method == "POST":
        form = PictureForm(request.POST, request.FILES, instance=Picture())
        if form.is_valid():
            form.save()
            return redirect(to="app_instagram:pictures")

    return render(request, "app_instagram/upload.html", context={"title": "Killer Instagram", "form": form})


def pictures(request):
    pictures = Picture.objects.all()  # noqa
    return render(request, "app_instagram/pictures.html", context={"title": "Killer Instagram", "pictures": []})