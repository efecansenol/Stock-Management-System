# Generated by Django 5.0.3 on 2024-04-20 11:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockmanagement', '0003_alter_stock_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='category',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='stockmanagement.category'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='item_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
