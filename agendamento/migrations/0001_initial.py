# Generated by Django 5.0 on 2023-12-30 14:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agendamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('hora', models.CharField(max_length=5)),
                ('dia', models.CharField(max_length=10)),
                ('jah_expirou', models.BooleanField()),
                ('codigo_estabelecimento', models.CharField(max_length=7)),
                ('nome_estabelecimento', models.CharField(max_length=150)),
                ('candidato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]