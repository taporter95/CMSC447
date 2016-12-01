# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('marketplace', '0004_post_post_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('payment', models.CharField(max_length=64)),
                ('buyerpaid', models.BooleanField(default=False)),
                ('sellerconfirmed', models.BooleanField(default=False)),
                ('seller', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('umbcid', models.CharField(max_length=7, serialize=False, primary_key=True)),
                ('rating', models.PositiveSmallIntegerField()),
                ('birth_date', models.DateField(null=True, blank=True)),
                ('gender', models.CharField(blank=True, max_length=8, choices=[('M', 'Male'), ('F', 'Female')])),
                ('location', models.CharField(max_length=200, blank=True)),
                ('banned', models.BooleanField(default=False)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.FileField(null=True, upload_to='uploads/', blank=True),
        ),
    ]
