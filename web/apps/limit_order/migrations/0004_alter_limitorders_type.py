# Generated by Django 4.0.6 on 2022-09-05 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('limit_order', '0003_limitorders_equivalentamount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='limitorders',
            name='type',
            field=models.CharField(choices=[('buy', 'buy'), ('sell', 'sell')], max_length=4),
        ),
    ]
