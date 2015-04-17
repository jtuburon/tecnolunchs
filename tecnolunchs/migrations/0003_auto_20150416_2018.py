# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tecnolunchs', '0002_transporter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transporter',
            name='user',
        ),
        migrations.DeleteModel(
            name='Transporter',
        ),
    ]
