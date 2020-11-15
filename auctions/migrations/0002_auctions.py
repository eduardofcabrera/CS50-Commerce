# Generated by Django 3.0.8 on 2020-08-01 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auctions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('image_url', models.URLField()),
                ('description', models.CharField(max_length=512)),
                ('firs_bid', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
    ]
