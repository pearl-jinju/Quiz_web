# Generated by Django 4.1.6 on 2023-03-02 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RankSurvive',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('stage', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='quizset',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='rank',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
