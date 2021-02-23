# Generated by Django 3.1.5 on 2021-02-15 23:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('keys', '0002_auto_20210216_0045'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='key',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='issues', to='keys.key', verbose_name='Schlüssel'),
        ),
    ]