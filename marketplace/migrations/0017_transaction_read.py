# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0016_auto_20161206_1810'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]
