# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0002_auto_20160709_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='privacy',
            field=models.BooleanField(default=True),
        ),
    ]
