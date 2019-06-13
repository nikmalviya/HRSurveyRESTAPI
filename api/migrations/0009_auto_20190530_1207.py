# Generated by Django 2.2.1 on 2019-05-30 12:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0008_auto_20190529_0556'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(unique=True)),
                ('required', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Question')),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('is_open', models.BooleanField(default=False)),
                ('questions', models.ManyToManyField(through='api.QuestionOrder', to='api.Question')),
            ],
        ),
        migrations.AddField(
            model_name='questionorder',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Survey'),
        ),
    ]
