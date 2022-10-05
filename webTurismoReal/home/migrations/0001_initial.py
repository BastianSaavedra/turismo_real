# Generated by Django 3.2.15 on 2022-10-05 15:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comuna',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name': 'Comuna',
                'verbose_name_plural': 'Comunas',
                'db_table': 'comuna',
            },
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100, null=True)),
                ('direccion', models.CharField(max_length=150)),
                ('descripcion', models.TextField()),
                ('comuna', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='home.comuna')),
            ],
            options={
                'verbose_name': 'Departamento',
                'verbose_name_plural': 'Departamentos',
                'db_table': 'departamento',
            },
        ),
        migrations.CreateModel(
            name='DetalleDpto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.PositiveBigIntegerField(default=0)),
                ('capacidad', models.IntegerField()),
                ('amoblado', models.CharField(choices=[('se', 'Seleccione'), ('SI', 'SI'), ('NO', 'NO')], default='se', max_length=2)),
                ('cable', models.CharField(choices=[('se', 'Seleccione'), ('SI', 'SI'), ('NO', 'NO')], default='se', max_length=2)),
                ('electronicos', models.CharField(choices=[('se', 'Seleccione'), ('SI', 'SI'), ('NO', 'NO')], default='se', max_length=2)),
                ('internet', models.CharField(choices=[('se', 'Seleccione'), ('SI', 'SI'), ('NO', 'NO')], default='se', max_length=2)),
                ('aire_acondicionado', models.CharField(choices=[('se', 'Seleccione'), ('SI', 'SI'), ('NO', 'NO')], default='se', max_length=2)),
                ('bodega', models.CharField(choices=[('se', 'Seleccione'), ('SI', 'SI'), ('NO', 'NO')], default='se', max_length=2)),
                ('bannio', models.CharField(choices=[('se', 'Seleccione'), ('SI', 'SI'), ('NO', 'NO')], default='se', max_length=2)),
                ('cant_bannio', models.PositiveIntegerField(default=0)),
                ('dormitorio', models.CharField(choices=[('se', 'Seleccione'), ('SI', 'SI'), ('NO', 'NO')], default='se', max_length=2)),
                ('cant_dormitorio', models.PositiveIntegerField(default=0)),
                ('estacionamiento', models.CharField(choices=[('se', 'Seleccione'), ('SI', 'SI'), ('NO', 'NO')], default='se', max_length=2)),
                ('cant_estacionamiento', models.PositiveIntegerField(default=0)),
                ('status', models.CharField(choices=[('1', 'disponible'), ('2', 'no disponible')], max_length=13)),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.departamento')),
            ],
            options={
                'verbose_name': 'Detalle departamento',
                'verbose_name_plural': 'Detalles de Departamentos',
                'db_table': 'detalle_dpto',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name': 'Region',
                'verbose_name_plural': 'Regiones',
                'db_table': 'region',
            },
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in', models.DateField()),
                ('check_out', models.DateField()),
                ('booking_id', models.CharField(default='null', max_length=100)),
                ('detalle_dpto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.detalledpto')),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Reserva',
                'verbose_name_plural': 'Reservas',
                'db_table': 'reserva',
            },
        ),
        migrations.AddField(
            model_name='comuna',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='home.region'),
        ),
    ]
