# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0014_auto_20161201_2013'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompleteTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('seller', models.CharField(max_length=200)),
                ('buyer', models.CharField(max_length=200)),
                ('postlabel', models.CharField(max_length=200)),
                ('payment_type', models.CharField(max_length=64)),
                ('buyerpaid', models.BooleanField(default=False)),
                ('sellerconfirmed', models.BooleanField(default=False)),
                ('notes', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='transaction',
            name='buyer',
            field=models.ForeignKey(related_name='buyer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='seller',
            field=models.ForeignKey(related_name='seller', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='rating',
            field=models.PositiveSmallIntegerField(default=5),
        ),
    ]
