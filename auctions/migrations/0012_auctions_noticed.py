# Generated by Django 3.0.8 on 2020-08-03 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_auctions_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctions',
            name='noticed',
            field=models.BooleanField(default=False),
        ),
    ]