# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-08-23 20:30
from __future__ import unicode_literals

from django.db.migrations import RunPython

from api.models.NotificationChannel import NotificationChannel
import api.notifications.notifications
import db_comments.model_mixins
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def create_notification_channels(apps, schema_editor):
    """
    Adds the IN-APP, SMS, and EMAIL communications channels, with default settings
    """
    db_alias = schema_editor.connection.alias

    channel = apps.get_model("api", "NotificationChannel")

    channel.objects.using(db_alias).bulk_create([
        channel(channel=NotificationChannel.AvailableChannels.IN_APP.name, enabled=True, subscribe_by_default=True),
        channel(channel=NotificationChannel.AvailableChannels.SMS.name, enabled=False, subscribe_by_default=False),
        channel(channel=NotificationChannel.AvailableChannels.EMAIL.name, enabled=True, subscribe_by_default=False)
    ])


def delete_notification_channels(apps, schema_editor):
    """
    Removes the historical data entry permission from the Government roles
    and deletes the actual permission.

    This is for reversing the migration.
    """
    db_alias = schema_editor.connection.alias

    channel = apps.get_model("api", "NotificationChannel")

    channel.objects.using(db_alias).filter(
        channel__in=[NotificationChannel.AvailableChannels.IN_APP.name,
                     NotificationChannel.AvailableChannels.SMS.name,
                     NotificationChannel.AvailableChannels.EMAIL.name]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_historical_data_entry_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_timestamp', models.DateTimeField(auto_now=True, null=True)),
                ('channel', models.CharField(choices=[(NotificationChannel.AvailableChannels('In-Application'), 'In-Application'), (NotificationChannel.AvailableChannels('SMS'), 'SMS'), (NotificationChannel.AvailableChannels('Email'), 'Email')], max_length=64, unique=True)),
                ('enabled', models.BooleanField()),
                ('subscribe_by_default', models.BooleanField()),
                ('create_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='api_notificationchannel_CREATE_USER', to=settings.AUTH_USER_MODEL)),
                ('update_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='api_notificationchannel_UPDATE_USER', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'notification_channel',
            },
            bases=(models.Model, db_comments.model_mixins.DBComments),
        ),
        migrations.CreateModel(
            name='NotificationMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_timestamp', models.DateTimeField(auto_now=True, null=True)),
                ('message', models.CharField(max_length=4000)),
                ('is_read', models.BooleanField(default=False)),
                ('is_warning', models.BooleanField(default=False)),
                ('is_error', models.BooleanField(default=False)),
                ('create_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='api_notificationmessage_CREATE_USER', to=settings.AUTH_USER_MODEL)),
                ('originating_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='notification_originating_user', to=settings.AUTH_USER_MODEL)),
                ('related_credit_trade', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='api.CreditTrade')),
                ('related_organization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='api.Organization')),
                ('related_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='notification_related_user', to=settings.AUTH_USER_MODEL)),
                ('update_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='api_notificationmessage_UPDATE_USER', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'notification_message',
            },
            bases=(models.Model, db_comments.model_mixins.DBComments),
        ),
        migrations.CreateModel(
            name='NotificationSubscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_timestamp', models.DateTimeField(auto_now=True, null=True)),
                ('notification_type', models.CharField(choices=[(api.notifications.notification_types.NotificationType('Credit Transfer Proposal Created'), 'Credit Transfer Proposal Created'), (api.notifications.notification_types.NotificationType('Credit Transfer Proposal Signed 1/2'), 'Credit Transfer Proposal Signed 1/2'), (api.notifications.notification_types.NotificationType('Credit Transfer Proposal Signed 2/2'), 'Credit Transfer Proposal Signed 2/2'), (api.notifications.notification_types.NotificationType('Credit Transfer Proposal Refused'), 'Credit Transfer Proposal Refused'), (api.notifications.notification_types.NotificationType('Credit Transfer Proposal Accepted'), 'Credit Transfer Proposal Accepted'), (api.notifications.notification_types.NotificationType('Credit Transfer Proposal Recommended For Approval'), 'Credit Transfer Proposal Recommended For Approval'), (api.notifications.notification_types.NotificationType('Credit Transfer Proposal Recommended For Declination'), 'Credit Transfer Proposal Recommended For Declination'), (api.notifications.notification_types.NotificationType('Credit Transfer Proposal Declined'), 'Credit Transfer Proposal Declined'), (api.notifications.notification_types.NotificationType('Credit Transfer Proposal Approved'), 'Credit Transfer Proposal Approved'), (api.notifications.notification_types.NotificationType('Credit Transfer Proposal Rescinded'), 'Credit Transfer Proposal Rescinded'), (api.notifications.notification_types.NotificationType('Credit Transfer Proposal Comment Created Or Updated'), 'Credit Transfer Proposal Comment Created Or Updated'), (api.notifications.notification_types.NotificationType('Credit Transfer Proposal Internal Comment Created Or Updated'), 'Credit Transfer Proposal Internal Comment Created Or Updated')], max_length=128)),
                ('enabled', models.BooleanField()),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.NotificationChannel')),
                ('create_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='api_notificationsubscription_CREATE_USER', to=settings.AUTH_USER_MODEL)),
                ('update_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='api_notificationsubscription_UPDATE_USER', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'notification_subscription',
            },
            bases=(models.Model, db_comments.model_mixins.DBComments),
        ),
        migrations.AlterUniqueTogether(
            name='notificationsubscription',
            unique_together=set([('user', 'channel', 'notification_type')]),
        ),
        RunPython(create_notification_channels, delete_notification_channels)
    ]