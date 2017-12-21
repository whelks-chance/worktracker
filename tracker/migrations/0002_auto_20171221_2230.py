# Generated by Django 2.0 on 2017-12-21 22:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectTimeAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hours', models.IntegerField()),
                ('financed', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='person',
            name='hours_per_week',
            field=models.IntegerField(default=35),
        ),
        migrations.AddField(
            model_name='projecttimeassignment',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.Person'),
        ),
        migrations.AddField(
            model_name='projecttimeassignment',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.Project'),
        ),
    ]