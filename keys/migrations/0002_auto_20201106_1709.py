# Generated by Django 3.0.7 on 2020-11-06 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keys', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='issues',
        ),
        migrations.AddField(
            model_name='person',
            name='issues',
            field=models.ManyToManyField(blank=True, related_name='person', to='keys.Issue', verbose_name='Ausgaben'),
        ),
    ]
