# Generated by Django 3.0.8 on 2020-08-03 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_auto_20200803_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctions',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
