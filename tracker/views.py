import json

from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render


# Create your views here.
from tracker import models


def explain(request):
    return render(request, 'explain.html',
                  {
                      'projects': models.Project.objects.all(),
                      'people': models.Person.objects.all(),
                      'funds': models.Fund.objects.all(),
                  }
                  )


def all_task_data(request):
    from tracker.checking.checking_inputs import Task
    tasks_data = {
        "task_data": Task.sanity_check_all()
    }
    return JsonResponse(tasks_data)


def all_people_data(request):

    all_time = models.ProjectTimeAssignment.objects.all()
    all_people = models.Person.objects.all()

    people_data = []
    for person in all_people:

        count = 0
        for ta in all_time:
            if ta.person == person:
                count += ta.hours

        people_data.append(
            {
                'count': count,
                'name': person.name,
                'id': person.id,
                'start_date': person.available_start_date,
                'end_date': person.available_end_date,
                'hours_per_week': person.hours_per_week
            }
        )

    api_data = {
        # 'all_time': list(all_time),
        'people_data': people_data
    }

    return JsonResponse(api_data)
