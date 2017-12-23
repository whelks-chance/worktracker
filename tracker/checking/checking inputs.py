import calendar
import os

import pytz

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "worktracker.settings")
import django
django.setup()

from django.db.models import Sum
from tracker import models
import datetime


class Checks:
    def check(self):
        proj = models.Project.objects.all()
        for p in proj:
            print('\n', p.name)
            print(p.__dict__)

            for task in p.task_set.all():
                print(task.name)

                for task_person in task.people_assigned.all():
                    print(task_person.name)

        print('\n')
        people = models.Person.objects.all()
        for pe in people:
            print('\n', pe.name)
            # print(pe.__dict__)

            print('\n', 'projects:', pe.projects.all().count())
            for person_proj in pe.projects.all():
                print(person_proj.name)


# feed this two tuples, ie overlaps((start, end), (start, end))
def overlaps(date1, date2):
    from datetime import datetime
    from collections import namedtuple
    Range = namedtuple('Range', ['start', 'end'])
    r1 = Range(start=date1[0], end=date1[1])
    r2 = Range(start=date2[0], end=date2[1])
    latest_start = max(r1.start, r2.start)
    earliest_end = min(r1.end, r2.end)
    overlap = (earliest_end - latest_start).days + 1
    return overlap


class WorkerPerson():
    def __init__(self, name):
        self.name = name

        self.db_person = models.Person.objects.get(name=self.name)
        if not self.db_person:
            raise()

    def hours_per_week(self):
        return self.db_person.hours_per_week

    def hours_per_year(self):
        return self.db_person.hours_per_week * 52

    def allocated_tasks_in_month(self, month_num, year):
        month_start = datetime.datetime(year, month_num, 1)
        month_start = pytz.utc.localize(month_start)

        month_end_day = calendar.monthrange(year, month_num)[1]
        month_end = datetime.datetime(year, month_num, month_end_day)
        month_end = pytz.utc.localize(month_end)

        person_allocations = models.ProjectTimeAssignment.objects.filter(person=self.db_person)
        print(person_allocations)

        total_time_assigned = person_allocations.aggregate(Sum('hours'))['hours__sum']

        tasks = []
        for allocation in person_allocations:
            project = allocation.project

            for project_task in project.task_set.all():
                print(project_task)

                # if project_task.start_date <= now_aware <= project_task.end_date:
                if overlaps((month_start, month_end), (project_task.start_date, project_task.end_date)):
                    tasks.append(project_task)
        return tasks


if __name__ == "__main__":
    c = Checks()
    c.check()
    print('\n\n')

    wp = WorkerPerson(name="Ian")
    print(wp.name, 'works', wp.hours_per_week(), 'hours per week.')
    print(wp.name, 'works', wp.hours_per_year(), 'hours per year.')

    print(wp.allocated_tasks_in_month(11, 2017))
