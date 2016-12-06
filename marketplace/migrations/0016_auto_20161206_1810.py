# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0015_auto_20161205_0251'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CompleteTransaction',
        ),
        migrations.AddField(
            model_name='transaction',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
