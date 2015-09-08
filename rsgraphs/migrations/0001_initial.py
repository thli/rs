# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_id', models.PositiveIntegerField()),
                ('name', models.CharField(default=b'', max_length=50)),
                ('dates', django.contrib.postgres.fields.ArrayField(base_field=models.DateField(), size=None)),
                ('prices', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=None)),
                ('volumes', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=None)),
                ('EMA_9', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=None)),
                ('MACD', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=None)),
                ('histogram', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=None)),
            ],
        ),
    ]
