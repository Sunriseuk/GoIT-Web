from django.db import models

# Create your models here.

class Author(models.Model):
    fullname = models.CharField(max_length=200, null=False, unique=True)
    born_date = models.DateField(null=False)
    born_location = models.CharField(max_length=200, null=False)
    description = models.TextField(null=False)

    def __str__(self):
        return self.fullname

class Tag(models.Model):
    name = models.CharField(max_length=30, null=False, unique=True)

    def __str__(self):
        return self.name

class Quote(models.Model):
    text = models.TextField(null=False)
    tags = models.ManyToManyField(Tag, related_name='quotes')

    author = models.ForeignKey(
        Author, on_delete=models.SET_NULL, null=True, related_name="quotes")
    
    def __str__(self):
        return f"{self.author.fullname}: '{self.text[:30]}...'"

