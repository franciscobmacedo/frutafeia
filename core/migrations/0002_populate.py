from django.db import migrations
from datetime import datetime as dt


def populate_needsMapaDeCampo(apps, schema):
    needsMapaDeCampo = apps.get_model("core", "PrecisaMapaDeCampo")
    needsMapaDeCampo.objects.all().delete()
    _ = needsMapaDeCampo.objects.create(value=True, date=dt.now())


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            code=populate_needsMapaDeCampo,
        )
    ]
