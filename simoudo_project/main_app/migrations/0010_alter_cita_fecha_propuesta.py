# Generated by Django 5.0.6 on 2024-06-13 01:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_alter_cita_fecha_propuesta_alter_doctor_user_ref'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cita',
            name='fecha_propuesta',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 14, 1, 19, 11, 170601, tzinfo=datetime.timezone.utc)),
        ),
    ]
