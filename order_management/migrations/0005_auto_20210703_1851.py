# Generated by Django 2.2 on 2021-07-03 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_management', '0004_auto_20210703_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(db_column='phone', max_length=50, unique=True),
        ),
    ]
