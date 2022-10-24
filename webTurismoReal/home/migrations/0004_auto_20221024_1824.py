# Generated by Django 3.2.15 on 2022-10-24 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_reserva_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='costo_multa',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='reserva',
            name='mensaje_check_in',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='reserva',
            name='mensaje_check_out',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='reserva',
            name='status_estadia',
            field=models.CharField(choices=[('0', 'Seleccionar'), ('1', 'Arribo'), ('2', 'No Arribo')], default='0', max_length=13),
        ),
    ]
