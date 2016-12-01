# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0006_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='post',
            field=models.ForeignKey(related_name='post', default=1, to='marketplace.Post'),
            preserve_default=False,
        ),
    ]
