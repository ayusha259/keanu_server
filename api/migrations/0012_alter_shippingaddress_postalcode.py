# Generated by Django 4.0.5 on 2022-06-25 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_rename_postalcode_shippingaddress_postalcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='postalcode',
            field=models.CharField(max_length=20),
        ),
    ]
