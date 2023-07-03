# Generated by Django 4.2.1 on 2023-05-08 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_rename_price_listings_initial_price_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='bid_counter',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='listings',
            name='current_amount',
            field=models.FloatField(default=0),
        ),
    ]
