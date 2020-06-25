# Generated by Django 3.0.7 on 2020-06-23 23:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('keys', '0015_auto_20200623_2318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='door',
            name='active',
            field=models.BooleanField(default=True, verbose_name='aktiv'),
        ),
        migrations.AlterField(
            model_name='door',
            name='comment',
            field=models.CharField(blank=True, max_length=64, verbose_name='kommentar'),
        ),
        migrations.AlterField(
            model_name='door',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='keys.Door'),
        ),
    ]
