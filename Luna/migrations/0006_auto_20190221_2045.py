# Generated by Django 2.1.7 on 2019-02-21 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Luna', '0005_auto_20190221_2001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='calendar',
            field=models.BinaryField(default=0),
        ),
    ]
