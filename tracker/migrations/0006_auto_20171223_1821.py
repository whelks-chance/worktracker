# Generated by Django 2.0 on 2017-12-23 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0005_fund_reference_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fund',
            name='reference_name',
            field=models.TextField(),
        ),
    ]
