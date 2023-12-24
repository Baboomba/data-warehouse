# Generated by Django 4.2.6 on 2023-12-24 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_alter_info_serial_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='info',
            old_name='product_info',
            new_name='product_id',
        ),
        migrations.AlterField(
            model_name='info',
            name='imei',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='info',
            name='serial_number',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='info',
            name='untact_solution',
            field=models.BigIntegerField(),
        ),
    ]
