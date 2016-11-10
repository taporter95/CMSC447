# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0003_auto_20161107_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_type',
            field=models.CharField(default='good', max_length=20),
            preserve_default=False,
        ),
    ]
