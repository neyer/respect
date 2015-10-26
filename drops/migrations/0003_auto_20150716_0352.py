# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drops', '0002_facebookpost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statement',
            name='timestamp',
            field=models.DecimalField(max_digits=16, decimal_places=2),
            preserve_default=True,
        ),
    ]
