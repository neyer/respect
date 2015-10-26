# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drops', '0005_auto_20150907_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='category',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
