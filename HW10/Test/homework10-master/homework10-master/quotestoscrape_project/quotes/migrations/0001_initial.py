# Generated by Django 4.1.6 on 2023-02-01 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=150)),
                ('born_date', models.CharField(max_length=100)),
                ('born_location', models.CharField(max_length=100)),
                ('born_description', models.CharField(max_length=10000)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quote', models.CharField(max_length=1500)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quotes.author')),
                ('tags', models.ManyToManyField(to='quotes.tag')),
            ],
        ),
    ]