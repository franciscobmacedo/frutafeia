from django.contrib import admin
from core import models
from django.apps import apps

app = apps.get_app_config("core")

for model_name, model in app.models.items():
    admin.site.register(model)
