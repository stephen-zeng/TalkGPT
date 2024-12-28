# Generated by Django 5.1.4 on 2024-12-28 13:36

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_remove_manual_id_remove_vad_id_manual_uuid_vad_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='instruction',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='conversation',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='conversation',
            name='vad_url',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='manual',
            name='message',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='manual',
            name='role',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='manual',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='manual',
            name='voice',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='vad',
            name='message',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='vad',
            name='role',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='vad',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='vad',
            name='voice',
            field=models.TextField(null=True),
        ),
    ]
