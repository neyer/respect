# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drops', '0004_auto_20150716_0541'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='aliases',
            field=models.ManyToManyField(related_name='aliases_rel_+', to='drops.Address'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='statement',
            name='source',
            field=models.CharField(default=b'', max_length=256),
            preserve_default=True,
        ),
    ]
