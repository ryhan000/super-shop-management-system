# Generated by Django 2.2 on 2021-07-03 18:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('product_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_column='created_at', default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
