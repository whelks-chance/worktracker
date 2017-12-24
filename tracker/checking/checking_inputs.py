import calendar
import os
import pprint

import pytz

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "worktracker.settings")
import django
django.setup()

from django.db.models import Sum, Min
from tracker import models
import datetime
from workdays import networkdays
from tracker.utils.utils import get_bank_holidays


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


class Person:
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

        project_ids = person_allocations.values_list('project_id', flat=True).distinct()
        print(list(project_ids))

        person_tasks = models.Task.objects.filter(people_assigned__in=(self.db_person,))

        print(person_tasks)

        project_tasks = []
        person_tasks_in_month = []

        for allocation in person_allocations:
            project = allocation.project

            for project_task in project.task_set.all():
                print(project_task)
                if overlaps((month_start, month_end), (project_task.start_date, project_task.end_date)):
                    project_tasks.append(project_task)

        for person_task in person_tasks:
            if overlaps((month_start, month_end), (person_task.start_date, person_task.end_date)):
                person_tasks_in_month.append(person_task)

        print(person_tasks_in_month)

        return project_tasks


def err(reason):
    return {
        "reason": reason
    }


class Task:

    @staticmethod
    def sanity_check_all():
        all_tasks = models.Task.objects.all()

        tasks_data = []
        for t in all_tasks:
            task = Task(t)
            errors = []
            task_data = {
                "id": t.id,
                "name": t.name,
                "fund": t.fund.reference_name,
                "people_assigned": list(t.people_assigned.values('id').annotate(name=Min('name')).values_list('name', flat=True)),
                "start_date": t.start_date.isoformat(),
                "end_date": t.end_date.isoformat(),
                "project": t.project.name,
                "preceding_tasks": list(t.preceding_tasks.values('id').annotate(name=Min('name')).values_list('name', flat=True)),
                "length_days": task.number_of_days(),
                "length_working_days": task.number_of_working_days()
            }

            if t.end_date < t.start_date:
                errors.append(err("Task ends before it starts"))

            task_data['errors'] = errors
            tasks_data.append(task_data)
        print(pprint.pformat(tasks_data))
        return tasks_data

    # We can create this with either a models.Task or the DB id
    def __init__(self, task):
        if isinstance(task, models.Task):
            self.db_task = task
        elif isinstance(task, int):
            self.db_task = models.Task.objects.get(id=task)
        else:
            raise Exception('Call Task with either model.Task object or DB id.')
        self.bank_holidays = list(get_bank_holidays())

    def number_of_days(self):
        return (self.db_task.end_date - self.db_task.start_date).days + 1

    def number_of_working_days(self):
        return networkdays(self.db_task.start_date, self.db_task.end_date, holidays=self.bank_holidays)


if __name__ == "__main__":
    c = Checks()
    c.check()
    print('\n\n')

    wp = Person(name="Ian")
    print(wp.name, 'works', wp.hours_per_week(), 'hours per week.')
    print(wp.name, 'works', wp.hours_per_year(), 'hours per year.')

    print(wp.allocated_tasks_in_month(11, 2017))

    t = Task(1)
    print('\nTask', t.db_task.name)
    print(t.number_of_days())
    print(t.number_of_working_days())

    t = Task(2)
    print('\nTask', t.db_task.name)
    print(t.number_of_days())
    print(t.number_of_working_days())

    t = Task(3)
    print('\nTask', t.db_task.name)
    print(t.number_of_days())
    print(t.number_of_working_days())

    t = Task(4)
    print('\nTask', t.db_task.name)
    print(t.number_of_days())
    print(t.number_of_working_days())

    Task.sanity_check_all()
