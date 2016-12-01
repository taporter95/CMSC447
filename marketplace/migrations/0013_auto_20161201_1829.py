# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0012_auto_20161201_1723'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='payment',
            new_name='payment_type',
        ),
        migrations.AddField(
            model_name='transaction',
            name='notes',
            field=models.CharField(default='note', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='post',
            field=models.ForeignKey(related_name='post', on_delete=django.db.models.deletion.PROTECT, default=1, to='marketplace.Post'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='status',
            field=models.CharField(default='active', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='buyer',
            field=models.ForeignKey(related_name='buyer', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='seller',
            field=models.ForeignKey(related_name='seller', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
