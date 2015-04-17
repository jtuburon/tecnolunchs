# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tecnolunchs', '0004_transportergroupmember'),
    ]

    operations = [
        migrations.AddField(
            model_name='transportergroupmember',
            name='transport_group',
            field=models.ForeignKey(default=1, to='tecnolunchs.TransporterGroup'),
            preserve_default=False,
        ),
    ]
