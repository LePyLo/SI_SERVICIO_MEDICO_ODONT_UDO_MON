# Generated by Django 5.0.6 on 2024-06-11 22:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_paciente_notas_alter_cita_fecha_propuesta'),
    ]

    operations = [
        migrations.AddField(
            model_name='asistente',
            name='notas',
            field=models.TextField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='doctor',
            name='notas',
            field=models.TextField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='medicamento',
            name='notas',
            field=models.TextField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='cita',
            name='fecha_propuesta',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 12, 22, 36, 32, 632291, tzinfo=datetime.timezone.utc)),
        ),
    ]
