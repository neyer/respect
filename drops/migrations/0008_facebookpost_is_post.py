# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drops', '0007_auto_20150930_0154'),
    ]

    operations = [
        migrations.AddField(
            model_name='facebookpost',
            name='is_post',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
