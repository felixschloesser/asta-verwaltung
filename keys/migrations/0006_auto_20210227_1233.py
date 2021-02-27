# Generated by Django 3.1.5 on 2021-02-27 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('keys', '0005_auto_20210227_1231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deposit',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deposits', to='keys.person', verbose_name='Person'),
        ),
    ]
