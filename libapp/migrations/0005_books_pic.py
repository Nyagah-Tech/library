# Generated by Django 2.2.8 on 2020-01-21 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libapp', '0004_auto_20200121_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='pic',
            field=models.ImageField(blank=True, upload_to='books/'),
        ),
    ]
