# Generated by Django 2.2.1 on 2019-05-28 10:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0005_auto_20190527_0935'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='is_multianswer_question',
            field=models.BooleanField(default=False),
        ),
    ]
