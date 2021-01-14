from django.db import models
from django.utils import timezone, text
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import (
    DateTimeRangeField,
    RangeBoundary,
    RangeOperators,
)

from phonenumber_field.modelfields import PhoneNumberField
from simple_history.models import HistoricalRecords
from hashid_field import HashidAutoField

from .validators import *
from .managers import *

# Create models here.
class Building(models.Model):
    identifier = models.CharField('Gebäude', max_length=8, unique=True)
    name = models.CharField('Name', max_length=32, unique=True, blank=True, null=True)
    created_at = models.DateTimeField('Erstellungszeitpunkt', auto_now_add=True)
    updated_at = models.DateTimeField('Aktualisierungszeitpunkt', auto_now=True)

    class Meta:
        verbose_name = "Gebäude"
        verbose_name_plural = "Gebäude"
        ordering = ['identifier']


    def __str__(self):
        if self.name:
            return "{} (Geb. {})".format(self.name, self.identifier)
        else:
            return self.identifier

    def get_number_of_rooms(self):
        return Room.objects.filter(building__identifier=self.identifier).count()

    get_number_of_rooms.short_description = "Anzahl Räume"



class Purpose(models.Model):
    name = models.CharField('Zweck', max_length=32)
    created_at = models.DateTimeField('Erstellungszeitpunkt', auto_now_add=True)
    updated_at = models.DateTimeField('Aktualisierungszeitpunkt', auto_now=True)

    class Meta:
        verbose_name = "Zweck"
        verbose_name_plural = "Zwecke"

    def __str__(self):
        return self.name



class Room(models.Model):
    building = models.ForeignKey('building',
                                  related_name='rooms',
                                  verbose_name='Gebäude',
                                  on_delete=models.CASCADE)
    number = models.CharField("Raumnummer", max_length=32)
    group = models.ForeignKey('group',
                               blank=True, null=True,
                               related_name='rooms',
                               verbose_name='Gruppe',
                               on_delete=models.PROTECT)
    name = models.CharField('Raumname', max_length=32, unique=True, blank=True, null=True)

    purpose = models.ForeignKey('purpose',
                                 verbose_name='Zweck',
                                 related_name='rooms',
                                 blank=True,
                                 null=True,
                                 on_delete=models.PROTECT)
    created_at = models.DateTimeField('Erstellungszeitpunkt', auto_now_add=True)
    updated_at = models.DateTimeField('Aktualisierungszeitpunkt', auto_now=True)

    class Meta:
        verbose_name = "Raum"
        verbose_name_plural = "Räume"

        constraints = [
            models.UniqueConstraint(fields=['building', 'number'],
                                    name='room_is_unique')
        ]


    def __str__(self):
        if self.name:
            return "{} ({})".format(self.name, self.number)
        else:
            return "{}{}".format(self.building.identifier, self.number)

    def get_identifier(self):
        return "{}{}".format(self.building.identifier, self.number)

    get_identifier.short_description = "Raumnummer"



class Door(models.Model):
    active = models.BooleanField("Aktiv", default=True)
    room = models.ForeignKey("Room", related_name="doors", verbose_name="führt in Raum",
                             on_delete=models.CASCADE)
    kind_choices = [('access', 'Zugangstüre'),
                    ('connecting', 'Verbindungstür')]
    kind = models.CharField('Typ', max_length=32, choices=kind_choices,
                             default=('access', 'Zugangstüre'))
    locking_system = models.ForeignKey('LockingSystem',
                                        related_name="doors",
                                        verbose_name='Schließsystem',
                                        on_delete = models.CASCADE)
    comment = models.CharField("Kommentar", max_length=64, blank=True, null=True)
    created_at = models.DateTimeField('Erstellungszeitpunkt', auto_now_add=True)
    updated_at = models.DateTimeField('Aktualisierungszeitpunkt', auto_now=True)

    class Meta:
        verbose_name = "Tür"
        verbose_name_plural = "Türen"

    def __str__(self):
        if self.kind == 'access':
            if self.room.name:
                return "Zugangstür zum {} ({})".format(self.room.name, self.room.number)
            else:
                return "Zugangstür zu {}".format(self.room.get_identifier())
        else:
            if self.room.name:
                return "Verbindungstür zum {} ({})".format(self.room.name, self.room.number)
            else:
                return "Verbindungstür zu {}".format(self.room.get_identifier())



class Key(models.Model):
    number = models.CharField("Schlüsselnummer", max_length=32)
    doors = models.ManyToManyField("Door", related_name='keys', verbose_name='Türen')
    locking_system = models.ForeignKey('LockingSystem',
                                        related_name='keys',
                                        verbose_name='Schließsystem',
                                        on_delete = models.CASCADE)
    storage_location = models.ForeignKey('StorageLocation',
                                          related_name='keys',
                                          verbose_name='Aufbewahrungsort',
                                          on_delete=models.PROTECT)
    stolen_or_lost = models.BooleanField('gestohlen oder verloren', default=False)

    created_at = models.DateTimeField('Erstellungszeitpunkt', auto_now_add=True)
    updated_at = models.DateTimeField('Aktualisierungszeitpunkt', auto_now=True)

    all_keys = KeyManager() # Custom manager to make methods accessible

    class Meta:
        verbose_name = "Schlüssel"
        verbose_name_plural = "Schlüssel"

        ordering = ['locking_system', 'number']

        indexes = [
            models.Index(fields=['number'], name='key_number_idx')
        ]

        constraints = [
            models.UniqueConstraint(fields=['number', 'locking_system'],
                                    name='key_number_in_locking_system_are_unique')
    ]

    def __str__(self):
        return self.number

    def get_absolute_url(self):
        return reverse('keys:key-detail', args=[str(self.id)])

    def get_current_issue(self):
        issue_set  = self.issues.active()
        try:
            issue = issue_set.get()
            return issue
        except ObjectDoesNotExist:
            return None

    def get_number_of_doors(self):
        return self.doors.all().count()

    def get_rooms(self):
        doors = self.doors.filter(kind__exact='access').distinct()
        rooms = [door.room for door in doors]
        return rooms

    def get_locking_system_method(self):
        return self.locking_system.method

        get_locking_system_method.short_description = 'Typ'
        get_number_of_doors.short_description = "Anzahl Türen"



class LockingSystem(models.Model):
    name = models.CharField(max_length=32, unique=True)
    method_choices = [('mechanical', 'mechanisch'),
                      ('mechatronical', 'mechatronisch'),
                      ('transponder', 'Transponder')]
    method = models.CharField('Schließverfahren', max_length=32,
                                       choices=method_choices,
                                       default=('mechanical', 'mechanisch'))
    company = models.CharField('Firma', max_length=32, unique=True, blank=True, null=True)
    comment = models.CharField('Kommentar', max_length=64, blank=True, null=True)
    created_at = models.DateTimeField('Erstellungszeitpunkt', auto_now_add=True)
    updated_at = models.DateTimeField('Aktualisierungszeitpunkt', auto_now=True)

    class Meta:
        verbose_name = "Schließsystem"
        verbose_name_plural = "Schließsysteme"

        constraints = [
            models.UniqueConstraint(fields=['name', 'company'],
                                    name='locking_system_is_unique')
        ]

    def __str__(self):
        return "{} von {}".format(self.name, self.company)



class StorageLocation(models.Model):
    name = models.CharField("Name", max_length=32)
    location = models.ForeignKey("room", related_name='storage_locations', verbose_name='Ort', on_delete=models.CASCADE)
    created_at = models.DateTimeField('Erstellungszeitpunkt', auto_now_add=True)
    updated_at = models.DateTimeField('Aktualisierungszeitpunkt', auto_now=True)

    class Meta:
        verbose_name = "Aufbewahrungsort"
        verbose_name_plural = "Aufbewahrungsorte"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_number_of_keys(self):
        return Key.objects.filter(storage_location__name=self.name).count()

    get_number_of_keys.short_description = "Anzahl Schlüssel"



class Person(models.Model): # Add a chron job ro delete after a 2 years of not renting?
    id = HashidAutoField(primary_key=True)

    first_name = models.CharField('Vorname', max_length=64)
    last_name = models.CharField('Nachname', max_length=64)
    university_email = models.EmailField('Uni-Mail', unique=True, validators=[validate_university_mail])
    private_email = models.EmailField('Private Mail', unique=True)
    phone_number = PhoneNumberField('Telefon', unique=True)
    group = models.ForeignKey('Group', related_name='people', verbose_name='Gruppe', on_delete=models.PROTECT, null=True)

    created_at = models.DateTimeField('Erstellungszeitpunkt', auto_now_add=True)
    updated_at = models.DateTimeField('Aktualisierungszeitpunkt', auto_now=True)

    all_people = PersonManager()

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "Personen"
        ordering = ['last_name', 'first_name', 'created_at']

        indexes = [
            models.Index(fields=['last_name', 'first_name']),
            models.Index(fields=['first_name'], name='first_name_idx'),
        ]

    def __str__(self):
        full_name = "{} {}".format(self.first_name, self.last_name)
        return full_name

    def get_absolute_url(self):
        return reverse('keys:person-detail', args=[str(self.id)])

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def has_paid_deposit(self):
        if hasattr(self, 'deposit') and not self.deposit.out_datetime:
            return True
        else:
            return False


    def get_active_issues(self):
        return self.issues.active()

    # Tell django-admin to display this as an Boolian
    has_paid_deposit.boolean = True
    has_paid_deposit.short_description = "Kaution"



class Deposit(models.Model):
    currency_choices = [('EUR', '€')]

    method_choices = [('cash', 'Bar'),
                      ('bank transfer', 'Überweisung')]

    person = models.OneToOneField('Person', verbose_name='Person', on_delete=models.PROTECT)
    amount = models.DecimalField('Kautionsbetrag', max_digits=5, decimal_places=2, default=50)

    currency = models.CharField('Währung', max_length=3, choices=currency_choices, default='EUR')


    in_datetime = models.DateTimeField('Einzahlungszeitpunkt', default=datetime.datetime.now, validators=[present_or_max_3_days_ago])
    in_method = models.CharField('Zahlungsmittel', max_length=64, choices=method_choices, default='cash')

    out_datetime = models.DateTimeField('Rückzahlungszeitpunkt', null=True, validators=[present_or_max_3_days_ago])
    out_method = models.CharField('Zahlungsmittel', max_length=64, choices=method_choices, null=True, default='cash')

    created_at = models.DateTimeField('Erstellungszeitpunkt', auto_now_add=True)
    updated_at = models.DateTimeField('Aktualisierungszeitpunkt', auto_now=True)

    class Meta:
        verbose_name = "Kaution"
        verbose_name_plural = "Kautionen"
        ordering = ["in_datetime", "amount"]

    def __str__(self):
        full_name = "{} {} von {}".format(self.amount, self.currency, self.person.get_full_name())
        return full_name

    def has_been_returned(self):
        if self.out_datetime and self.out_method:
            return True
        else:
            return False

    has_been_returned.boolean = True
    has_been_returned.short_description = "Zurückgegeben"


class Group(models.Model):
    name = models.CharField('Name', max_length=64, unique=True)
    created_at = models.DateTimeField('Erstellungszeitpunkt', auto_now_add=True)
    updated_at = models.DateTimeField('Aktualisierungszeitpunkt', auto_now=True)

    class Meta:
        verbose_name = "Gruppe"
        verbose_name_plural = "Gruppen"
        ordering = ['id']

    def __str__(self):
        return "{}".format(self.name)



class Issue(models.Model):
    active = models.BooleanField(verbose_name='Aktiv', default=True)
    person = models.ForeignKey('Person',
                               related_name="issues",
                               verbose_name='Ausgaben',
                               on_delete=models.PROTECT)
    #limit_key_choices = models.Q(issues__active=False, stolen_or_lost=False)
    #!BUG duplication https://code.djangoproject.com/ticket/11707
    # still not fixed in 3.1.5?

    key = models.ForeignKey('Key', related_name="issues",
                            verbose_name='Schlüssel',
                            on_delete=models.PROTECT)
                            #limit_choices_to=limit_key_choices)

    out_date = models.DateField('Ausgabedatum',
                                default=timezone.now,
                                validators=[present_or_max_10_days_ago])
    in_date = models.DateField('Rückgabedatum',
                                null=True, blank=True,
                                validators=[present_or_max_10_days_ago])
    created_at = models.DateTimeField('Erstellungszeitpunkt', auto_now_add=True)
    updated_at = models.DateTimeField('Aktualisierungszeitpunkt', auto_now=True)

    all_issues = IssueManager()

    id = HashidAutoField(primary_key=True)

    class Meta:
        verbose_name='Ausleihe'
        verbose_name_plural='Ausleihen'
        ordering = ['-out_date']

        constraints = [
            models.UniqueConstraint(
                name='key_not_yet_returned',
                fields=['key'],
                condition=models.Q(active=True),
            ),
            models.CheckConstraint(
                name='only_inacrive_have_in_date',
                check=models.Q(active=True, in_date__isnull=True) | \
                      models.Q(active=False, in_date__isnull=False)
            ),
            models.CheckConstraint(
                name='give_out_before_take_in',
                check=models.Q(in_date__gte=models.F('out_date')),
            ),
        ]

    def __str__(self):
        return "{} an {}".format(self.key, self.person)

    def get_absolute_url(self):
        return reverse('keys:issue-detail', args=[str(self.id)])




