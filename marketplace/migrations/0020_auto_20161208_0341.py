# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0019_post_hourly'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='buyer_canceled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='transaction',
            name='seller_relisted',
            field=models.BooleanField(default=False),
        ),
    ]
