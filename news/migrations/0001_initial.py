# Generated by Django 3.1.1 on 2020-10-11 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('text', models.CharField(max_length=1048576)),
                ('title', models.CharField(max_length=256)),
                ('link', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
    ]
