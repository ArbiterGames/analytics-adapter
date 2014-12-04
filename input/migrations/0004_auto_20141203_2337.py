# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('input', '0003_auto_20141117_2359'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlgorithmRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('version', models.CharField(max_length=10)),
                ('value', models.CharField(default=b'0', max_length=10)),
                ('record', models.ForeignKey(blank=True, to='input.Record', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='record',
            name='dau',
            field=models.CharField(default=b'0', max_length=100, verbose_name=b'DAU'),
            preserve_default=True,
        ),
    ]
