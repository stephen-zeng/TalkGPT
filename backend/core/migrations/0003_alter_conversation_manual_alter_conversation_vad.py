# Generated by Django 5.1.4 on 2024-12-17 14:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_conversation_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='manual',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversations', to='core.manual'),
        ),
        migrations.AlterField(
            model_name='conversation',
            name='vad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversations', to='core.vad'),
        ),
    ]