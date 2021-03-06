# Generated by Django 2.2.8 on 2020-01-24 05:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('libapp', '0011_borrowing_notification'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification', tinymce.models.HTMLField()),
                ('posted_on', models.DateTimeField(auto_now_add=True)),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
