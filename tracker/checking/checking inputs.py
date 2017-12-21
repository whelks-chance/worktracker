import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "worktracker.settings")
import django
django.setup()

from tracker import models


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



if __name__ == "__main__":
    c = Checks()
    c.check()