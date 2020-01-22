# Generated by Django 2.2.8 on 2020-01-22 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libapp', '0005_books_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='borrowing',
            name='no_of_books',
            field=models.IntegerField(default=0),
        ),
    ]
