# Generated by Django 2.0 on 2017-12-24 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0006_auto_20171223_1821'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='hours_per_week',
            field=models.IntegerField(default=35),
        ),
    ]