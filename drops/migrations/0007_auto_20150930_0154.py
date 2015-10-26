# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drops', '0006_address_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='facebookpost',
            name='post_body',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='facebookpost',
            name='reply',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
    ]
