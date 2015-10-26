# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drops', '0003_auto_20150716_0352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statement',
            name='value',
            field=models.DecimalField(default=0, max_digits=6, decimal_places=4),
            preserve_default=True,
        ),
    ]
