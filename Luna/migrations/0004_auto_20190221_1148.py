# Generated by Django 2.1.7 on 2019-02-21 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Luna', '0003_auto_20190221_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='school',
            field=models.CharField(default='School', max_length=256),
        ),
        migrations.AlterField(
            model_name='user',
            name='url',
            field=models.CharField(default='Url', max_length=256),
        ),
    ]
