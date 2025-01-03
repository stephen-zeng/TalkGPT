# Generated by Django 5.1.4 on 2025-01-03 12:58

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_conversation_instruction_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vad',
            name='conversation',
        ),
        migrations.RemoveField(
            model_name='conversation',
            name='manual_free',
        ),
        migrations.RemoveField(
            model_name='conversation',
            name='vad_free',
        ),
        migrations.RemoveField(
            model_name='conversation',
            name='vad_url',
        ),
        migrations.AddField(
            model_name='conversation',
            name='model',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='conversation',
            name='temperature',
            field=models.DecimalField(decimal_places=1, max_digits=2, null=True),
        ),
        migrations.AddField(
            model_name='conversation',
            name='vad',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Memory',
            fields=[
                ('role', models.BooleanField(default=False)),
                ('message', models.TextField(null=True)),
                ('voice', models.TextField(null=True)),
                ('time', models.DateTimeField(auto_now=True)),
                ('serverID', models.TextField(null=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('conversation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='memory', to='core.conversation')),
            ],
        ),
        migrations.DeleteModel(
            name='Manual',
        ),
        migrations.DeleteModel(
            name='VAD',
        ),
    ]
