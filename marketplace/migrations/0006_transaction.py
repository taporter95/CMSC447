# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('marketplace', '0005_auto_20161128_2042'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=20)),
                ('buyer', models.ForeignKey(related_name='buyer', to=settings.AUTH_USER_MODEL)),
                ('seller', models.ForeignKey(related_name='seller', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
