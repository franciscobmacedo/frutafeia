# Generated by Django 3.2.2 on 2021-06-23 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_cesta_conteudocesta'),
    ]

    operations = [
        migrations.CreateModel(
            name='CestaResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.BooleanField()),
                ('message', models.TextField()),
            ],
        ),
    ]