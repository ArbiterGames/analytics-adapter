# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('input', '0002_auto_20141117_1748'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='prize_pool_impact',
            field=models.CharField(default=b'0', max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='record',
            name='dau',
            field=models.CharField(default=b'0', max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='record',
            name='revenue',
            field=models.CharField(default=b'0', max_length=100),
            preserve_default=True,
        ),
    ]
