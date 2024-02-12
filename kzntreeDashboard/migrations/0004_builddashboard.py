# Generated by Django 5.0.2 on 2024-02-12 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kzntreeDashboard', '0003_remove_inventoryitem_available_stock_status_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuildDashboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('references', models.CharField(max_length=255)),
                ('item_group', models.CharField(max_length=255)),
                ('quantity', models.PositiveIntegerField()),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('linked_sale_order_group', models.CharField(max_length=255)),
                ('creation_group_date', models.DateField()),
                ('completion_group_date', models.DateField()),
            ],
        ),
    ]
