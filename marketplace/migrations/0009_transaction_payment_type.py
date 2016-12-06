# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0008_post_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='payment_type',
            field=models.CharField(default='none', max_length=20),
            preserve_default=False,
        ),
    ]
