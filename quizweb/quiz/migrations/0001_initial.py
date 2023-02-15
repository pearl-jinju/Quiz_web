# Generated by Django 4.1.6 on 2023-02-13 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QuizSet',
            fields=[
                ('quiz_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('category', models.TextField()),
                ('price', models.IntegerField()),
                ('img_url', models.TextField()),
                ('url', models.TextField()),
                ('num', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='rank',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('stage', models.IntegerField()),
                ('point', models.IntegerField()),
            ],
        ),
    ]
