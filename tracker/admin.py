from django.contrib import admin
from django.apps import apps

# Register your models here.

# Add all the regular models to admin
for model in apps.get_app_config('tracker').get_models():
    try:
        admin.site.register(model)
    except:
        pass