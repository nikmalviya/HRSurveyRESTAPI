# Generated by Django 2.2.1 on 2019-05-28 13:18

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0006_question_is_multianswer_question'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='answer_required',
            new_name='required',
        ),
    ]