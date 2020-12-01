# Generated by Django 3.1.3 on 2020-11-29 15:59

import datetime
from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions
import django.utils.timezone
import djmoney.models.fields
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
            name='Deposit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_currency', djmoney.models.fields.CurrencyField(choices=[('XUA', 'ADB Unit of Account'), ('AFN', 'Afghani'), ('DZD', 'Algerian Dinar'), ('ARS', 'Argentine Peso'), ('AMD', 'Armenian Dram'), ('AWG', 'Aruban Guilder'), ('AUD', 'Australian Dollar'), ('AZN', 'Azerbaijanian Manat'), ('BSD', 'Bahamian Dollar'), ('BHD', 'Bahraini Dinar'), ('THB', 'Baht'), ('PAB', 'Balboa'), ('BBD', 'Barbados Dollar'), ('BYN', 'Belarussian Ruble'), ('BYR', 'Belarussian Ruble'), ('BZD', 'Belize Dollar'), ('BMD', 'Bermudian Dollar (customarily known as Bermuda Dollar)'), ('BTN', 'Bhutanese ngultrum'), ('VEF', 'Bolivar Fuerte'), ('BOB', 'Boliviano'), ('XBA', 'Bond Markets Units European Composite Unit (EURCO)'), ('BRL', 'Brazilian Real'), ('BND', 'Brunei Dollar'), ('BGN', 'Bulgarian Lev'), ('BIF', 'Burundi Franc'), ('XOF', 'CFA Franc BCEAO'), ('XAF', 'CFA franc BEAC'), ('XPF', 'CFP Franc'), ('CAD', 'Canadian Dollar'), ('CVE', 'Cape Verde Escudo'), ('KYD', 'Cayman Islands Dollar'), ('CLP', 'Chilean peso'), ('XTS', 'Codes specifically reserved for testing purposes'), ('COP', 'Colombian peso'), ('KMF', 'Comoro Franc'), ('CDF', 'Congolese franc'), ('BAM', 'Convertible Marks'), ('NIO', 'Cordoba Oro'), ('CRC', 'Costa Rican Colon'), ('HRK', 'Croatian Kuna'), ('CUP', 'Cuban Peso'), ('CUC', 'Cuban convertible peso'), ('CZK', 'Czech Koruna'), ('GMD', 'Dalasi'), ('DKK', 'Danish Krone'), ('MKD', 'Denar'), ('DJF', 'Djibouti Franc'), ('STD', 'Dobra'), ('DOP', 'Dominican Peso'), ('VND', 'Dong'), ('XCD', 'East Caribbean Dollar'), ('EGP', 'Egyptian Pound'), ('SVC', 'El Salvador Colon'), ('ETB', 'Ethiopian Birr'), ('EUR', 'Euro'), ('XBB', 'European Monetary Unit (E.M.U.-6)'), ('XBD', 'European Unit of Account 17(E.U.A.-17)'), ('XBC', 'European Unit of Account 9(E.U.A.-9)'), ('FKP', 'Falkland Islands Pound'), ('FJD', 'Fiji Dollar'), ('HUF', 'Forint'), ('GHS', 'Ghana Cedi'), ('GIP', 'Gibraltar Pound'), ('XAU', 'Gold'), ('XFO', 'Gold-Franc'), ('PYG', 'Guarani'), ('GNF', 'Guinea Franc'), ('GYD', 'Guyana Dollar'), ('HTG', 'Haitian gourde'), ('HKD', 'Hong Kong Dollar'), ('UAH', 'Hryvnia'), ('ISK', 'Iceland Krona'), ('INR', 'Indian Rupee'), ('IRR', 'Iranian Rial'), ('IQD', 'Iraqi Dinar'), ('IMP', 'Isle of Man Pound'), ('JMD', 'Jamaican Dollar'), ('JOD', 'Jordanian Dinar'), ('KES', 'Kenyan Shilling'), ('PGK', 'Kina'), ('LAK', 'Kip'), ('KWD', 'Kuwaiti Dinar'), ('AOA', 'Kwanza'), ('MMK', 'Kyat'), ('GEL', 'Lari'), ('LVL', 'Latvian Lats'), ('LBP', 'Lebanese Pound'), ('ALL', 'Lek'), ('HNL', 'Lempira'), ('SLL', 'Leone'), ('LSL', 'Lesotho loti'), ('LRD', 'Liberian Dollar'), ('LYD', 'Libyan Dinar'), ('SZL', 'Lilangeni'), ('LTL', 'Lithuanian Litas'), ('MGA', 'Malagasy Ariary'), ('MWK', 'Malawian Kwacha'), ('MYR', 'Malaysian Ringgit'), ('TMM', 'Manat'), ('MUR', 'Mauritius Rupee'), ('MZN', 'Metical'), ('MXV', 'Mexican Unidad de Inversion (UDI)'), ('MXN', 'Mexican peso'), ('MDL', 'Moldovan Leu'), ('MAD', 'Moroccan Dirham'), ('BOV', 'Mvdol'), ('NGN', 'Naira'), ('ERN', 'Nakfa'), ('NAD', 'Namibian Dollar'), ('NPR', 'Nepalese Rupee'), ('ANG', 'Netherlands Antillian Guilder'), ('ILS', 'New Israeli Sheqel'), ('RON', 'New Leu'), ('TWD', 'New Taiwan Dollar'), ('NZD', 'New Zealand Dollar'), ('KPW', 'North Korean Won'), ('NOK', 'Norwegian Krone'), ('PEN', 'Nuevo Sol'), ('MRO', 'Ouguiya'), ('TOP', 'Paanga'), ('PKR', 'Pakistan Rupee'), ('XPD', 'Palladium'), ('MOP', 'Pataca'), ('PHP', 'Philippine Peso'), ('XPT', 'Platinum'), ('GBP', 'Pound Sterling'), ('BWP', 'Pula'), ('QAR', 'Qatari Rial'), ('GTQ', 'Quetzal'), ('ZAR', 'Rand'), ('OMR', 'Rial Omani'), ('KHR', 'Riel'), ('MVR', 'Rufiyaa'), ('IDR', 'Rupiah'), ('RUB', 'Russian Ruble'), ('RWF', 'Rwanda Franc'), ('XDR', 'SDR'), ('SHP', 'Saint Helena Pound'), ('SAR', 'Saudi Riyal'), ('RSD', 'Serbian Dinar'), ('SCR', 'Seychelles Rupee'), ('XAG', 'Silver'), ('SGD', 'Singapore Dollar'), ('SBD', 'Solomon Islands Dollar'), ('KGS', 'Som'), ('SOS', 'Somali Shilling'), ('TJS', 'Somoni'), ('SSP', 'South Sudanese Pound'), ('LKR', 'Sri Lanka Rupee'), ('XSU', 'Sucre'), ('SDG', 'Sudanese Pound'), ('SRD', 'Surinam Dollar'), ('SEK', 'Swedish Krona'), ('CHF', 'Swiss Franc'), ('SYP', 'Syrian Pound'), ('BDT', 'Taka'), ('WST', 'Tala'), ('TZS', 'Tanzanian Shilling'), ('KZT', 'Tenge'), ('XXX', 'The codes assigned for transactions where no currency is involved'), ('TTD', 'Trinidad and Tobago Dollar'), ('MNT', 'Tugrik'), ('TND', 'Tunisian Dinar'), ('TRY', 'Turkish Lira'), ('TMT', 'Turkmenistan New Manat'), ('TVD', 'Tuvalu dollar'), ('AED', 'UAE Dirham'), ('XFU', 'UIC-Franc'), ('USD', 'US Dollar'), ('USN', 'US Dollar (Next day)'), ('UGX', 'Uganda Shilling'), ('CLF', 'Unidad de Fomento'), ('COU', 'Unidad de Valor Real'), ('UYI', 'Uruguay Peso en Unidades Indexadas (URUIURUI)'), ('UYU', 'Uruguayan peso'), ('UZS', 'Uzbekistan Sum'), ('VUV', 'Vatu'), ('CHE', 'WIR Euro'), ('CHW', 'WIR Franc'), ('KRW', 'Won'), ('YER', 'Yemeni Rial'), ('JPY', 'Yen'), ('CNY', 'Yuan Renminbi'), ('ZMK', 'Zambian Kwacha'), ('ZMW', 'Zambian Kwacha'), ('ZWD', 'Zimbabwe Dollar A/06'), ('ZWN', 'Zimbabwe dollar A/08'), ('ZWL', 'Zimbabwe dollar A/09'), ('PLN', 'Zloty')], default='EUR', editable=False, max_length=3)),
                ('amount', djmoney.models.fields.MoneyField(decimal_places=2, default=Decimal('50'), default_currency='EUR', max_digits=5, verbose_name='Kautionsbetrag')),
                ('in_datetime', models.DateTimeField(default=datetime.datetime.now, verbose_name='Einzahlungszeitpunkt')),
                ('in_method', models.CharField(choices=[('cash', 'Bargeld'), ('bank transfer', 'Überweisung'), ('other payment provider', 'anderer Zahlungsdienstleister')], default='cash', max_length=64, verbose_name='Einzahlungsmittel')),
                ('out_datetime', models.DateTimeField(blank=True, null=True, verbose_name='Rückzahlungszeitpunkt')),
                ('out_method', models.CharField(blank=True, choices=[('cash', 'Bargeld'), ('bank transfer', 'Überweisung'), ('other payment provider', 'anderer Zahlungsdienstleister')], max_length=64, null=True, verbose_name='Rückzahlungsmittel')),
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
                ('comment', models.CharField(blank=True, max_length=64, null=True, verbose_name='Kommentar')),
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
                ('out_date', models.DateField(default=django.utils.timezone.now, validators=[keys.models.present_or_max_10_days_ago], verbose_name='Ausgabedatum')),
                ('in_date', models.DateField(blank=True, null=True, validators=[keys.models.present_or_max_10_days_ago], verbose_name='Rückgabedatum')),
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
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='keys.building', verbose_name='Gebäude')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='rooms', to='keys.group', verbose_name='Gruppe')),
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
                ('first_name', models.CharField(max_length=64, verbose_name='Vorname')),
                ('last_name', models.CharField(max_length=64, verbose_name='Nachname')),
                ('university_email', models.EmailField(max_length=254, unique=True, validators=[keys.models.validate_university_mail], verbose_name='Uni-Mail')),
                ('private_email', models.EmailField(max_length=254, unique=True, verbose_name='Private Mail')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True, verbose_name='Telefon')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Erstellungszeitpunkt')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Aktualisierungszeitpunkt')),
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', min_length=7, primary_key=True, serialize=False)),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='people', to='keys.group', verbose_name='Gruppe')),
            ],
            options={
                'verbose_name': 'Person',
                'verbose_name_plural': 'Personen',
                'ordering': ['last_name', 'first_name', 'created_at'],
            },
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
            constraint=models.UniqueConstraint(fields=('number', 'locking_system'), name='key_number+locking_system_is_unique'),
        ),
        migrations.AddConstraint(
            model_name='issue',
            constraint=models.CheckConstraint(check=models.Q(in_date__gte=django.db.models.expressions.F('out_date')), name='give_out_before_take_in'),
        ),
    ]
