# Generated by Django 2.2.1 on 2019-05-30 12:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0009_auto_20190530_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='start_date',
            field=models.DateField(null=True),
        ),
    ]