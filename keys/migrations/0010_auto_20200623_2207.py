# Generated by Django 3.0.7 on 2020-06-23 22:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('keys', '0009_door_doors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='door',
            name='doors',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='keys.Door'),
        ),
    ]
