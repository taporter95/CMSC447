# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0010_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='gender',
            field=models.CharField(max_length=8, blank=True),
        ),
    ]
