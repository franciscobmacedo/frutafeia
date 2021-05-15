# Generated by Django 3.2.2 on 2021-05-15 20:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210515_2111'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='familiaproduto',
            options={'verbose_name': 'Família de Produto', 'verbose_name_plural': 'Famílias de Produtos'},
        ),
        migrations.CreateModel(
            name='Disponibilidade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('delegacao', models.CharField(max_length=255)),
                ('quantidade', models.FloatField()),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.produto')),
                ('produtor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.produtor')),
            ],
        ),
    ]