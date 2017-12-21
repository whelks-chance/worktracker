from django.shortcuts import render


# Create your views here.
from tracker import models


def explain(request):
    return render(request, 'explain.html',
                  {
                      'projects': models.Project.objects.all(),
                  }
                  )
