# Generated by Django 3.0.8 on 2020-08-01 21:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20200801_2131'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auctions',
            old_name='name',
            new_name='Title',
        ),
    ]