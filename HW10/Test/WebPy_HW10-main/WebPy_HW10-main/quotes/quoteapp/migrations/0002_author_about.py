# Generated by Django 4.1.3 on 2023-02-05 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quoteapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='about',
            field=models.TextField(blank=True),
        ),
    ]
