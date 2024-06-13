# Generated by Django 5.0.6 on 2024-06-13 01:39

import datetime
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_alter_cita_fecha_propuesta'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicamento',
            name='creado_en',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cita',
            name='fecha_propuesta',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 14, 1, 39, 8, 958223, tzinfo=datetime.timezone.utc)),
        ),
    ]