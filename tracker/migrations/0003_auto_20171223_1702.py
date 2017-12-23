# Generated by Django 2.0 on 2017-12-23 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_auto_20171221_2230'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('costed_hours', models.IntegerField()),
                ('description_of_intent', models.TextField()),
                ('cash', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FundingBody',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('department', models.TextField()),
                ('account_number', models.IntegerField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='objectives',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='task',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='fund',
            name='funding_body',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.FundingBody'),
        ),
    ]