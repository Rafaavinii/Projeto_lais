# Generated by Django 5.0 on 2024-01-06 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agendamento', '0003_remove_agendamento_codigo_estabelecimento_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='agendamento',
            name='minuto',
            field=models.CharField(default='12', max_length=2),
            preserve_default=False,
        ),
    ]
