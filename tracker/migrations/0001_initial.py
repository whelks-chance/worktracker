# Generated by Django 2.0 on 2017-12-21 21:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('available_start_date', models.DateTimeField(verbose_name='employment_start_date')),
                ('available_end_date', models.DateTimeField(verbose_name='employment_end_date')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('start_date', models.DateTimeField(null=True, verbose_name='start date')),
                ('end_date', models.DateTimeField(null=True, verbose_name='end date')),
                ('principal_investigator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tracker.Person')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('start_date', models.DateTimeField(verbose_name='start date')),
                ('end_date', models.DateTimeField(verbose_name='end date')),
                ('people_assigned', models.ManyToManyField(related_name='assigned_to', to='tracker.Person')),
                ('preceding_tasks', models.ManyToManyField(related_name='preceding', to='tracker.Task')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.Project')),
                ('subsequent_tasks', models.ManyToManyField(related_name='subsequent', to='tracker.Task')),
            ],
        ),
        migrations.AddField(
            model_name='person',
            name='projects',
            field=models.ManyToManyField(to='tracker.Project'),
        ),
    ]
