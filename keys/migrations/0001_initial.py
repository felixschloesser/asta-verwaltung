# Generated by Django 3.0.7 on 2020-11-09 18:24

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions
import django.db.models.manager
import django.utils.timezone
import hashid_field.field
import keys.models
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
            name='Door',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, verbose_name='Aktiv')),
                ('kind', models.CharField(choices=[('access', 'Zugangstüre'), ('connecting', 'Verbindungstür')], default=('access', 'Zugangstüre'), max_length=32, verbose_name='Typ')),
                ('comment', models.CharField(blank=True, max_length=64, verbose_name='Kommentar')),
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
                ('out_date', models.DateField(default=django.utils.timezone.now, validators=[keys.models.present_or_past_date], verbose_name='Ausgabedatum')),
                ('in_date', models.DateField(blank=True, null=True, validators=[keys.models.present_or_past_date], verbose_name='Rückgabedatum')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Erstellungszeitpunkt')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Aktualisierungszeitpunkt')),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Ausleihe',
                'verbose_name_plural': 'Ausleihen',
                'ordering': ['-out_date'],
            },
        ),
        migrations.CreateModel(
            name='Key',
            fields=[
                ('number', models.CharField(max_length=32, verbose_name='Schlüsselnummer')),
                ('stolen_or_lost', models.BooleanField(default=False, verbose_name='gestohlen oder verloren')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Erstellungszeitpunkt')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Aktualisierungszeitpunkt')),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Schlüssel',
                'verbose_name_plural': 'Schlüssel',
                'ordering': ['locking_system', 'number'],
            },
        ),
        migrations.CreateModel(
            name='LockingSystem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('method', models.CharField(choices=[('mechanical', 'mechanisch'), ('mechatronical', 'mechatronisch'), ('transponder', 'Transponder')], default=('mechanical', 'mechanisch'), max_length=32, verbose_name='Schließverfahren')),
                ('company', models.CharField(blank=True, max_length=32, null=True, unique=True, verbose_name='Firma')),
                ('comment', models.CharField(blank=True, max_length=64, null=True, verbose_name='Kommentar')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Erstellungszeitpunkt')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Aktualisierungszeitpunkt')),
            ],
            options={
                'verbose_name': 'Schließsystem',
                'verbose_name_plural': 'Schließsysteme',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=32, verbose_name='Raumnummer')),
                ('name', models.CharField(blank=True, max_length=32, null=True, unique=True, verbose_name='Raumname')),
                ('purpose', models.CharField(choices=[('committee', 'Gremienraum'), ('office', 'Büroraum'), ('seminar', 'Seminarraum'), ('storage', 'Lager'), ('event location', 'Veranstaltungslocation'), ('multipurpose', 'Mehrzweckraum'), ('hallway', 'Flur'), ('other', 'Anderer')], max_length=32, verbose_name='Zweck')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Erstellungszeitpunkt')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Aktualisierungszeitpunkt')),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='keys.Building', verbose_name='Gebäude')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='keys.Group', verbose_name='Gruppe')),
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
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='keys.Room', verbose_name='Ort')),
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
                ('first_name', models.CharField(max_length=64, verbose_name='Vorname')),
                ('last_name', models.CharField(max_length=64, verbose_name='Nachname')),
                ('university_email', models.EmailField(max_length=254, unique=True, validators=[keys.models.validate_university_mail], verbose_name='Uni-Mail')),
                ('private_email', models.EmailField(max_length=254, unique=True, verbose_name='Private Mail')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True, verbose_name='Telefon')),
                ('deposit_paid', models.BooleanField(default=False, verbose_name='Kaution hinterlegt')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Erstellungszeitpunkt')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Aktualisierungszeitpunkt')),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='keys.Group', verbose_name='Gruppe')),
            ],
            options={
                'verbose_name': 'Person',
                'verbose_name_plural': 'Personen',
                'ordering': ['last_name', 'first_name'],
            },
            managers=[
                ('issues', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddConstraint(
            model_name='lockingsystem',
            constraint=models.UniqueConstraint(fields=('name', 'company'), name='locking_system_is_unique'),
        ),
        migrations.AddField(
            model_name='key',
            name='doors',
            field=models.ManyToManyField(to='keys.Door', verbose_name='Türen'),
        ),
        migrations.AddField(
            model_name='key',
            name='locking_system',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='keys.LockingSystem', verbose_name='Schließsystem'),
        ),
        migrations.AddField(
            model_name='key',
            name='storage_location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='keys.StorageLocation', verbose_name='Aufbewahrungsort'),
        ),
        migrations.AddField(
            model_name='issue',
            name='keys',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='keys.Key', verbose_name='Schlüssel'),
        ),
        migrations.AddField(
            model_name='issue',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='issue', to='keys.Person', verbose_name='Ausgaben'),
        ),
        migrations.AddField(
            model_name='door',
            name='locking_system',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='keys.LockingSystem', verbose_name='Schließsystem'),
        ),
        migrations.AddField(
            model_name='door',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='keys.Room', verbose_name='führt in Raum'),
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
            constraint=models.UniqueConstraint(fields=('number', 'locking_system'), name='key_number+locking_system_is_unique'),
        ),
        migrations.AddConstraint(
            model_name='issue',
            constraint=models.CheckConstraint(check=models.Q(in_date__gte=django.db.models.expressions.F('out_date')), name='give_out_before_take_in'),
        ),
    ]
