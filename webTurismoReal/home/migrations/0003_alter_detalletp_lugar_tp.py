# Generated by Django 3.2.15 on 2022-11-11 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_detalletp_lugar_tp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalletp',
            name='lugar_tp',
            field=models.CharField(blank=True, default='Seleccionar', max_length=200, null=True),
        ),
    ]
