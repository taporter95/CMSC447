# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0013_auto_20161201_1829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='post',
            field=models.ForeignKey(related_name='post', to='marketplace.Post'),
        ),
    ]
