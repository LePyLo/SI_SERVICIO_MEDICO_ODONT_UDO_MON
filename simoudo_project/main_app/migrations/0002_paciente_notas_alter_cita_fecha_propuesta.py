# Generated by Django 5.0.6 on 2024-06-11 22:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='notas',
            field=models.TextField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='cita',
            name='fecha_propuesta',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 12, 22, 35, 18, 198253, tzinfo=datetime.timezone.utc)),
        ),
    ]
