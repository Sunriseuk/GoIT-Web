from django.db import models

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        return f'{self.name}'


class Author(models.Model):
    fullname = models.CharField(max_length=100, unique=True)
    born_date = models.CharField(max_length=150, null=False)
    born_location = models.CharField(max_length=100, null=False)
    description = models.TextField(null=False)

    def __str__(self):
        return f'{self.fullname}'


class Quote(models.Model):
    text = models.TextField(unique=True, null=False)
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.text}: {self.author}, {self.tags}"
