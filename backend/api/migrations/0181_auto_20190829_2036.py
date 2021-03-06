# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-08-29 20:36
from __future__ import unicode_literals

import api.models.SigningAuthorityAssertion
from django.db import migrations, models

from api.models.SigningAuthorityAssertion import SigningAuthorityAssertion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0180_add_director_compliance_report_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signingauthorityassertion',
            name='module',
            field=models.CharField(choices=[(SigningAuthorityAssertion.AssertionModules('credit_trade'), 'CREDIT_TRADE'), (SigningAuthorityAssertion.AssertionModules('compliance_report'), 'COMPLIANCE_REPORTING'), (SigningAuthorityAssertion.AssertionModules('exclusion_report'), 'EXCLUSION_REPORTS')], default='credit_trade', max_length=50),
        ),
    ]
