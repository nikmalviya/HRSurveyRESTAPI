# Generated by Django 2.2.1 on 2019-05-27 06:24

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200)),
                ('question_type', models.CharField(
                    choices=[('short_answer', 'Short Answer'), ('multiple_choice', 'Multiple Choice'),
                             ('check_boxes', 'Check Boxes'), ('paragraph', 'Paragraph')], max_length=50)),
                ('required', models.BooleanField(default=False)),
            ],
        ),
    ]
