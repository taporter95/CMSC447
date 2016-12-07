# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0017_transaction_read'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='read',
            new_name='buyer_read',
        ),
        migrations.AddField(
            model_name='transaction',
            name='seller_read',
            field=models.BooleanField(default=False),
        ),
    ]
