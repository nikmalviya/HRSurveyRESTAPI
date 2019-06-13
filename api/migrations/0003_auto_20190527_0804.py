# Generated by Django 2.2.1 on 2019-05-27 08:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0002_questionchoice'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='required',
            new_name='answer_required',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='question_type',
            new_name='input_type',
        ),
        migrations.AddField(
            model_name='question',
            name='multiple_choice_answer',
            field=models.BooleanField(default=False),
        ),
    ]
