# Generated by Django 4.0.6 on 2022-08-15 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0003_remove_tradehistory_price_alter_tradehistory_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='cryptoName',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='tradehistory',
            name='amount',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='tradehistory',
            name='pair',
            field=models.CharField(max_length=255),
        ),
    ]
