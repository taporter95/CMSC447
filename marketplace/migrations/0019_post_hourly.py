# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0018_auto_20161207_1955'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='hourly',
            field=models.BooleanField(default=False),
        ),
    ]
