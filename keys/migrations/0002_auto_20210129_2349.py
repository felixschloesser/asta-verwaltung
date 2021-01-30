# Generated by Django 3.1.5 on 2021-01-29 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keys', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='deposit',
            name='in_deposit_no_out_datetime_out_method',
        ),
        migrations.AlterField(
            model_name='deposit',
            name='state',
            field=models.CharField(choices=[('in', 'Eingezahlt'), ('retained', 'Einbehalten'), ('out', 'Ausgezahlt')], default='in', max_length=8, verbose_name='Status'),
        ),
        migrations.AddConstraint(
            model_name='deposit',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('out_datetime__isnull', True), ('out_method__isnull', True), ('retained_datetime__isnull', True), ('state', 'in')), models.Q(('out_datetime__isnull', True), ('out_method__isnull', True), ('retained_datetime__isnull', False), ('state', 'retained')), models.Q(('out_datetime__isnull', False), ('out_method__isnull', False), ('state', 'out')), _connector='OR'), name='state_consistancy'),
        ),
    ]