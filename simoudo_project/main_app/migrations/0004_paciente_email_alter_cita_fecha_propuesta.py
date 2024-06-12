# Generated by Django 5.0.6 on 2024-06-11 22:48

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_asistente_notas_doctor_notas_medicamento_notas_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='email',
            field=models.CharField(blank=True, max_length=255, validators=[django.core.validators.EmailValidator()]),
        ),
        migrations.AlterField(
            model_name='cita',
            name='fecha_propuesta',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 12, 22, 48, 5, 223714, tzinfo=datetime.timezone.utc)),
        ),
    ]
