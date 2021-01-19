# Generated by Django 3.1.5 on 2021-01-19 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keys', '0010_auto_20210119_1549'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='deposit',
            name='inactive_deposit_no_in_method',
        ),
        migrations.RemoveConstraint(
            model_name='deposit',
            name='inactive_deposit_no_out_datetime',
        ),
        migrations.RemoveConstraint(
            model_name='issue',
            name='inactive_issue_no_in_date',
        ),
        migrations.AddConstraint(
            model_name='deposit',
            constraint=models.CheckConstraint(check=models.Q(('active', True), ('out_datetime__isnull', True), ('out_method__isnull', True)), name='active_deposit_no_out_datetime_out_method'),
        ),
        migrations.AddConstraint(
            model_name='deposit',
            constraint=models.CheckConstraint(check=models.Q(('active', False), ('out_datetime__isnull', False), ('out_method__isnull', True)), name='inactive_deposit_has_out_datetime_out_method'),
        ),
        migrations.AddConstraint(
            model_name='issue',
            constraint=models.CheckConstraint(check=models.Q(('active', True), ('in_date__isnull', True)), name='active_issue_no_in_date'),
        ),
        migrations.AddConstraint(
            model_name='issue',
            constraint=models.CheckConstraint(check=models.Q(('active', False), ('in_date__isnull', False)), name='inactive_issue_has_in_date'),
        ),
    ]
