# Generated by Django 4.1.6 on 2023-02-15 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quoteapp", "0004_rename_qoute_quote_quote"),
    ]

    operations = [
        migrations.AlterField(
            model_name="author",
            name="bio",
            field=models.CharField(max_length=4000),
        ),
    ]
