# Generated by Django 3.2.15 on 2022-10-19 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalledpto',
            name='status',
            field=models.CharField(choices=[('1', 'disponible'), ('2', 'mantencion')], max_length=13),
        ),
    ]
