# Generated by Django 4.2.1 on 2023-05-08 06:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_listings_bid_counter_listings_current_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listings',
            old_name='bid_counter',
            new_name='bid_count',
        ),
    ]
