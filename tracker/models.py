from django.db import models

# Create your models here.


class Person(models.Model):
    name = models.CharField(max_length=200)
    available_start_date = models.DateTimeField('employment_start_date')
    available_end_date = models.DateTimeField('employment_end_date')


class Project(models.Model):
    name = models.CharField(max_length=200)
    principal_investigator = Person()
    start_date = models.DateTimeField('start date')
    end_date = models.DateTimeField('end date')


class ProjectTeam(models.Model):
    project = Project()
    person = Person()


class Task(models.Model):
    name = models.CharField(max_length=200)
    people_assigned = models.ManyToManyField(Person, 'assigned_to')
    start_date = models.DateTimeField('start date')
    end_date = models.DateTimeField('end date')
    project_team = ProjectTeam()
    preceding_tasks = models.ManyToManyField('Task', related_name='preceding')
    subsequent_tasks = models.ManyToManyField('Task', related_name='subsequent')
