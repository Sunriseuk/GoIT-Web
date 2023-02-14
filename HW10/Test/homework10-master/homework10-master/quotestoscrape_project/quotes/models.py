from django.db import models

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=25)
    
    def __str__(self) -> str:
        return self.name
    
class Author(models.Model):
    fullname = models.CharField(max_length=150)
    born_date = models.CharField(max_length=100)
    born_location = models.CharField(max_length=100)
    born_description = models.CharField(max_length=10000)
    
    def __str__(self) -> str:
        return self.fullname
    
class Quote(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    quote = models.CharField(max_length=1500)
    tags = models.ManyToManyField(Tag)
    
    def __str__(self) -> str:
        return self.quote
    
    
