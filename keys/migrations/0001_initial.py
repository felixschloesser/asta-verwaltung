# Generated by Django 3.1.3 on 2021-01-27 12:00

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions
import django.db.models.manager
import django.utils.timezone
import hashid_field.field
import keys.validators
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=8, unique=True, verbose_name='Gebäude')),
                ('name', models.CharField(blank=True, max_length=32, null=True, unique=True, verbose_name='Name')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Erstellungszeitpunkt')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Aktualisierungszeitpunkt')),
            ],
            options={
                'verbose_name': 'Gebäude',
                'verbose_name_plural': 'Gebäude',
                'ordering': ['identifier'],
            },
        ),
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Aktiv')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, default=50, max_digits=5, validators=[keys.validators.validate_deposit_mail], verbose_name='Kautionsbetrag')),
                ('currency', models.CharField(choices=[('EUR', '€')], default='EUR', max_length=3, verbose_name='Währung')),
                ('in_datetime', models.DateTimeField(default=django.utils.timezone.now, validators=[keys.validators.present_or_max_3_days_ago], verbose_name='Einzahlungszeitpunkt')),
                ('in_method', models.CharField(choices=[('cash', 'Bar'), ('bank_transfer', 'Überweisung')], default='cash', max_length=64, verbose_name='Zahlungsmittel')),
                ('out_datetime', models.DateTimeField(null=True, validators=[keys.validators.present_or_max_3_days_ago], verbose_name='Rückzahlungszeitpunkt')),
                ('out_method', models.CharField(choices=[('cash', 'Bar'), ('bank_transfer', 'Überweisung')], max_length=64, null=True, verbose_name='Zahlungsmittel')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Erstellungszeitpunkt')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Aktualisierungszeitpunkt')),
            ],
            options={
                'verbose_name': 'Kaution',
                'verbose_name_plural': 'Kautionen',
                'ordering': ['in_datetime', 'amount'],
            },
        ),
        migrations.CreateModel(
            name='Door',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Aktiv')),
                ('kind', models.CharField(choices=[('access', 'Zugangstüre'), ('connecting', 'Verbindungstür')], default=('access', 'Zugangstüre'), max_length=32, verbose_name='Typ')),
                ('comment', models.CharField(blank=True, max_length=500, null=True, verbose_name='Kommentar')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Erstellungszeitpunkt')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Aktualisierungszeitpunkt')),
            ],
            options={
                'verbose_name': 'Tür',
                'verbose_name_plural': 'Türen',
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Name')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Erstellungszeitpunkt')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Aktualisierungszeitpunkt')),
            ],
            options={
                'verbose_name': 'Gruppe',
                'verbose_name_plural': 'Gruppen',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('active', models.BooleanField(default=True, verbose_name='Aktiv')),
                ('out_date', models.DateField(default=django.utils.timezone.now, validators=[keys.validators.present_or_max_10_days_ago], verbose_name='Ausgabedatum')),
                ('in_date', models.DateField(null=True, validators=[keys.validators.present_or_max_10_days_ago], verbose_name='Rückgabedatum')),
                ('comment', models.CharField(blank=True, max_length=500, null=True, verbose_name='Kommentar')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Erstellungszeitpunkt')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Aktualisierungszeitpunkt')),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Ausleihe',
                'verbose_name_plural': 'Ausleihen',
                'ordering': ['-out_date'],
            },
            managers=[
                ('all_issues', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Key',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=32, verbose_name='Schlüsselnummer')),
                ('stolen_or_lost', models.BooleanField(default=False, verbose_name='gestohlen oder verloren')),
                ('comment', models.CharField(blank=True, max_length=500, null=True, verbose_name='Kommentar')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Erstellungszeitpunkt')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Aktualisierungszeitpunkt')),
            ],
            options={
                'verbose_name': 'Schlüssel',
                'verbose_name_plural': 'Schlüssel',
                'ordering': ['locking_system', 'number'],
            },
            managers=[
                ('all_keys', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='LockingSystem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('method', models.CharField(choices=[('mechanical', 'mechanisch'), ('mechatronical', 'mechatronisch'), ('transponder', 'Transponder')], default=('mechanical', 'mechanisch'), max_length=32, verbose_name='Schließverfahren')),
                ('company', models.CharField(blank=True, max_length=32, null=True, unique=True, verbose_name='Firma')),
                ('comment', models.CharField(blank=True, max_length=500, null=True, verbose_name='Kommentar')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Erstellungszeitpunkt')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Aktualisierungszeitpunkt')),
            ],
            options={
                'verbose_name': 'Schließsystem',
                'verbose_name_plural': 'Schließsysteme',
            },
        ),
        migrations.CreateModel(
            name='Purpose',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='Zweck')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Erstellungszeitpunkt')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Aktualisierungszeitpunkt')),
            ],
            options={
                'verbose_name': 'Zweck',
                'verbose_name_plural': 'Zwecke',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=32, verbose_name='Raumnummer')),
                ('name', models.CharField(blank=True, max_length=32, null=True, unique=True, verbose_name='Raumname')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Erstellungszeitpunkt')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Aktualisierungszeitpunkt')),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='keys.building', verbose_name='Gebäude')),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='rooms', to='keys.group', verbose_name='Gruppe')),
                ('purpose', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='rooms', to='keys.purpose', verbose_name='Zweck')),
            ],
            options={
                'verbose_name': 'Raum',
                'verbose_name_plural': 'Räume',
            },
        ),
        migrations.CreateModel(
            name='StorageLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='Name')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Erstellungszeitpunkt')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Aktualisierungszeitpunkt')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='storage_locations', to='keys.room', verbose_name='Ort')),
            ],
            options={
                'verbose_name': 'Aufbewahrungsort',
                'verbose_name_plural': 'Aufbewahrungsorte',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=64, verbose_name='Vorname')),
                ('last_name', models.CharField(max_length=64, verbose_name='Nachname')),
                ('university_email', models.EmailField(max_length=254, unique=True, validators=[keys.validators.validate_university_mail], verbose_name='Uni-Mail')),
                ('private_email', models.EmailField(max_length=254, unique=True, verbose_name='Private Mail')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True, verbose_name='Telefon')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Erstellungszeitpunkt')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Aktualisierungszeitpunkt')),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='people', to='keys.group', verbose_name='Gruppe')),
            ],
            options={
                'verbose_name': 'Person',
                'verbose_name_plural': 'Personen',
                'ordering': ['last_name', 'first_name', 'created_at'],
            },
            managers=[
                ('all_people', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddConstraint(
            model_name='lockingsystem',
            constraint=models.UniqueConstraint(fields=('name', 'company'), name='locking_system_is_unique'),
        ),
        migrations.AddField(
            model_name='key',
            name='doors',
            field=models.ManyToManyField(related_name='keys', to='keys.Door', verbose_name='Türen'),
        ),
        migrations.AddField(
            model_name='key',
            name='locking_system',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='keys', to='keys.lockingsystem', verbose_name='Schließsystem'),
        ),
        migrations.AddField(
            model_name='key',
            name='storage_location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='keys', to='keys.storagelocation', verbose_name='Aufbewahrungsort'),
        ),
        migrations.AddField(
            model_name='issue',
            name='key',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='issues', to='keys.key', verbose_name='Schlüssel'),
        ),
        migrations.AddField(
            model_name='issue',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='issues', to='keys.person', verbose_name='Ausgaben'),
        ),
        migrations.AddField(
            model_name='door',
            name='locking_system',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doors', to='keys.lockingsystem', verbose_name='Schließsystem'),
        ),
        migrations.AddField(
            model_name='door',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doors', to='keys.room', verbose_name='führt in Raum'),
        ),
        migrations.AddField(
            model_name='deposit',
            name='person',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='keys.person', verbose_name='Person'),
        ),
        migrations.AddConstraint(
            model_name='room',
            constraint=models.UniqueConstraint(fields=('building', 'number'), name='room_is_unique'),
        ),
        migrations.AddIndex(
            model_name='person',
            index=models.Index(fields=['last_name', 'first_name'], name='keys_person_last_na_101fc1_idx'),
        ),
        migrations.AddIndex(
            model_name='person',
            index=models.Index(fields=['first_name'], name='first_name_idx'),
        ),
        migrations.AddIndex(
            model_name='key',
            index=models.Index(fields=['number'], name='key_number_idx'),
        ),
        migrations.AddConstraint(
            model_name='key',
            constraint=models.UniqueConstraint(fields=('number', 'locking_system'), name='key_number_in_locking_system_are_unique'),
        ),
        migrations.AddConstraint(
            model_name='issue',
            constraint=models.UniqueConstraint(condition=models.Q(active=True), fields=('key',), name='key_not_yet_returned'),
        ),
        migrations.AddConstraint(
            model_name='issue',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('active', True), ('in_date__isnull', True)), models.Q(('active', False), ('in_date__isnull', False)), _connector='OR'), name='active_issue_no_in_date'),
        ),
        migrations.AddConstraint(
            model_name='issue',
            constraint=models.CheckConstraint(check=models.Q(out_date__lte=django.db.models.expressions.F('in_date')), name='give_out_key_before_take_in'),
        ),
        migrations.AddConstraint(
            model_name='deposit',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('active', True), ('out_datetime__isnull', True), ('out_method__isnull', True)), models.Q(('active', False), ('out_datetime__isnull', False), ('out_method__isnull', False)), _connector='OR'), name='active_deposit_no_out_datetime_out_method'),
        ),
        migrations.AddConstraint(
            model_name='deposit',
            constraint=models.CheckConstraint(check=models.Q(in_datetime__lte=django.db.models.expressions.F('out_datetime')), name='take_in_deposit_before_give_out'),
        ),
        migrations.AddConstraint(
            model_name='deposit',
            constraint=models.CheckConstraint(check=models.Q(amount__gte=0), name='deposit_not_negative'),
        ),
    ]
