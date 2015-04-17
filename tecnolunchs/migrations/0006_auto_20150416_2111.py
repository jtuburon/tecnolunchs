# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tecnolunchs', '0005_transportergroupmember_transport_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='transportergroupmember',
            name='checked_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 16, 21, 11, 40, 366802, tzinfo=utc), verbose_name=b'datetime checked'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transportergroupmember',
            name='transport_group',
            field=models.ForeignKey(related_name='members', to='tecnolunchs.TransporterGroup'),
        ),
    ]
