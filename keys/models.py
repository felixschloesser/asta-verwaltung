from django.db import models
from django.utils import timezone, text
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import (
    DateTimeRangeField,
    RangeBoundary,
    RangeOperators,
)

from django_extensions.validators import NoWhitespaceValidator, NoControlCharactersValidator

from phonenumber_field.modelfields import PhoneNumberField
from simple_history.models import HistoricalRecords
from hashid_field import HashidAutoField
from autoslug import AutoSlugField

from .validators import *
from .managers import *

import logging

# Slug Functions

# Room
def get_room_slug(instance):
    return '%s-%s' % (instance.building.identifier, instance.number)


# Models
class Group(models.Model):
    name = models.CharField('Name', max_length=64, unique=True)
    created_at = models.DateTimeField('Erstellungszeitpunkt', auto_now_add=True)
    updated_at = models.DateTimeField('Aktualisierungszeitpunkt', auto_now=True)

    objects = GroupManager()

    class Meta:
        verbose_name = "Gruppe"
        verbose_name_plural = "Gruppen"
        ordering = ['id']

    def __str__(self):
        return "{}".format(self.name)



class Building(models.Model):
    identifier = models.CharField('Gebäudekürzel', max_length=8, unique=True)
    name = models.CharField('Name', max_length=32, unique=True, blank=True, null=True)
    created_at = models.DateTimeField('Erstellungszeitpunkt', auto_now_add=True)
    updated_at = models.DateTimeField('Aktualisierungszeitpunkt', auto_now=True)

    objects = BuildingManager()

    class Meta:
        verbose_name = "Gebäude"
        verbose_name_plural = "Gebäude"
        ordering = ['identifier']


    def __str__(self):
        if self.name:
            return "{}\xa0(Geb.\xa0{})".format(self.name, self.identifier)
        else:
            return "Gebäude\xa0{}".format(self.identifier)

    def get_rooms(self):
        return Room.objects.filter(building__identifier=self.identifier)


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
    number = models.CharField("Raumnummer", help_text='Ohne Gebäudekürzel: E0.069 -> 0.069', max_length=32)
    group = models.ForeignKey('group',
                               blank=True, null=True,
                               related_name='rooms',
                               verbose_name='Gruppe',
                               on_delete=models.PROTECT)
    purpose = models.ForeignKey('purpose',
                                 verbose_name='Zweck',
                                 related_name='rooms',
                                 help_text='Für FSRe&AStA wird automatisch ein Name aus Gruppe und Zweck generiert. "FSR VT" + "Lager" -> "FSR VT LAGER"',
                                 blank=True,
                                 null=True,
                                 on_delete=models.PROTECT)
    name = models.CharField('Raumname', max_length=32, unique=True, blank=True, null=True)

    comment = models.CharField("Kommentar", max_length=500, blank=True, null=True)

    slug = AutoSlugField(populate_from=get_room_slug, unique=True)

    created_at = models.DateTimeField('Erstellungszeitpunkt', auto_now_add=True)
    updated_at = models.DateTimeField('Aktualisierungszeitpunkt', auto_now=True)

    objects = RoomManager()

    class Meta:
        verbose_name = "Raum"
        verbose_name_plural = "Räume"

        constraints = [
            models.UniqueConstraint(fields=['building', 'number'],
                                    name='room_is_unique')
        ]


    def __str__(self):
        if self.name:
            name_string = "{}\xa0({})".format(self.name, self.number)
        elif self.purpose.name == 'Gremienraum' and self.group.name in Group.objects.fsr_list():
            name_string = "{}\xa0({})".format(self.group, self.number)
        elif self.purpose.name != 'Gremienraum' and self.group.name in Group.objects.fsr_list():
            name_string = "{}\xa0{}\xa0({})".format(self.group, self.purpose, self.number)
        elif self.group.name == 'AStA':
            name_string = "{}\xa0{}\xa0({})".format(self.group, self.purpose, self.number)
        elif self.group.name == 'StuPa':
            name_string = "{}\xa0{}\xa0({})".format(self.group, self.purpose, self.number)
        else:
            name_string = "{}{}".format(self.building.identifier, self.number)

        return name_string

    def get_absolute_url(self):
        return reverse('keys:room-detail', kwargs={'slug': self.slug})

    def get_short_name(self):
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
    kind_choices = [('access', 'Zugangstür'),
                    ('connecting', 'Verbindungstür')]
    kind = models.CharField('Typ', max_length=32, choices=kind_choices,
                             default=('access', 'Zugangstüre'))
    locking_system = models.ForeignKey('LockingSystem',
                                        related_name="doors",
                                        verbose_name='Schließsystem',
                                        on_delete = models.CASCADE)
    comment = models.CharField("Kommentar", max_length=500, blank=True, null=True)
    created_at = models.DateTimeField('Erstellungszeitpunkt', auto_now_add=True)
    updated_at = models.DateTimeField('Aktualisierungszeitpunkt', auto_now=True)

    class Meta:
        verbose_name = "Tür"
        verbose_name_plural = "Türen"

    def __str__(self):
        if self.kind == 'access':
            if self.room.name:
                return "Zugangstür zum\xa0{}\xa0({})".format(self.room.name, self.room.number)
            else:
                return "Zugangstür zu\xa0{}".format(self.room.get_identifier())
        else:
            if self.room.name:
                return "Verbindungstür zum\xa0{}\xa0({})".format(self.room.name, self.room.number)
            else:
                return "Verbindungstür zu\xa0{}".format(self.room.get_identifier())

    def get_kind(self):
        if self.kind == 'access':
            return "Zugangstür"
        elif self.kind == 'connecting':
            return "Verbindungstür"
        else:
            logging.error("Invalid door type: {}".format(self.kind))
            raise ValueError("Invalid door type")



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

    comment = models.CharField("Kommentar", max_length=500, blank=True, null=True)

    created_at = models.DateTimeField('Erstellungszeitpunkt', auto_now_add=True)
    updated_at = models.DateTimeField('Aktualisierungszeitpunkt', auto_now=True)

    objects = KeyManager() # Custom manager to make methods accessible

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
        if self.locking_system.method == 'transponder':
            return "Transponder Nr.\xa0{}".format(self.number)
        else:
            return "Schlüssel Nr.\xa0{}".format(self.number)

    def get_absolute_url(self):
        return reverse('keys:key-detail', args=[str(self.id)])

    def get_current_issue(self):
        """
        If the key is currently issued, return the issue instance,
        otherwise return Null.
        """
        issue_set = self.issues.active()
        if issue_set:
            issue = issue_set.get()
            return issue
        else:
            logging.error("Key not currently Issued")
            return None

    def is_currently_issued(self):
        """
        If the key is currently issued, return True,
        otherwise return False. Used in admin.
        """
        if self.issues.active():
            return True
        else:
            return False

    def get_number_of_doors(self):
        return self.doors.all().count()

    def get_rooms(self):
        doors = self.doors.filter(kind__exact='access').distinct()
        rooms = [door.room for door in doors]
        return rooms

    def get_locking_system_method(self):
        return self.locking_system.method

    def get_building(self):
        doors = self.doors.filter(kind__exact='access').distinct()
        rooms = [door.room for door in doors]
        return rooms

    # Provide short_discription/translation and meta information for django admin.
    get_locking_system_method.short_description = 'Typ'
    get_number_of_doors.short_description = "Anzahl Türen"

    is_currently_issued.boolean = True
    is_currently_issued.short_description = "Ausgeliehen"


class LockingSystem(models.Model):
    name = models.CharField(max_length=32, unique=True)
    method_choices = [('mechanical', 'mechanisch'),
                      ('mechatronical', 'mechatronisch'),
                      ('transponder', 'Transponder')]
    method = models.CharField('Schließverfahren', max_length=32,
                                       choices=method_choices,
                                       default=('mechanical', 'mechanisch'))
    company = models.CharField('Firma', max_length=32, unique=True, blank=True, null=True)
    comment = models.CharField('Kommentar', max_length=500, blank=True, null=True)

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
        if self.company:
            return "{} von\xa0{}".format(self.name, self.company)
        else:
            return self.name

    def get_method(self):
        """
        Sadly Django does not seem to provide a good way
        to access the fields verbose name.
        """
        if self.method == 'mechanical':
            return "mechanisch"

        elif self.method == 'mechatronical':
            return "mechatronisch"

        elif self.method == 'transponder':
            return "Transponder"
        else:
            logging.error("Unknown locking-system method: {}".format(self.method))
            raise ValueError("Unkown locking-system mehod")



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

    # Provide short_discription/translation for django admin.
    get_number_of_keys.short_description = "Anzahl Schlüssel"



class Person(models.Model): # Add a chron job ro delete after a 2 years of not renting?
    id = HashidAutoField(primary_key=True)

    first_name = models.CharField('Vorname', max_length=64, validators=[NoControlCharactersValidator,
                                                                        NoWhitespaceValidator])
    last_name = models.CharField('Nachname', max_length=64, validators=[NoControlCharactersValidator,
                                                                        NoWhitespaceValidator])
    university_email = models.EmailField('Uni Mail', unique=True, validators=[validate_university_mail])
    private_email = models.EmailField('Private Mail', unique=True)
    phone_number = PhoneNumberField('Telefon', unique=True)
    group = models.ForeignKey('Group', related_name='people', verbose_name='Gruppe', on_delete=models.PROTECT, null=True)

    gdpr_consent = models.BooleanField('Zustimmung Datenverarbeitung')

    history = HistoricalRecords()

    created_at = models.DateTimeField('Erstellungszeitpunkt', auto_now_add=True)
    updated_at = models.DateTimeField('Aktualisierungszeitpunkt', auto_now=True)

    objects = PersonManager()

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "Personen"
        ordering = ['last_name', 'first_name', 'created_at']

        indexes = [
            models.Index(fields=['last_name', 'first_name']),
            models.Index(fields=['first_name'], name='first_name_idx'),
        ]

        constraints = [
            models.CheckConstraint(
                name='emails_not_the_same',
                # ~ == NOT
                check=~models.Q(university_email__iexact=models.F('private_email'))
            )
        ]

    def __str__(self):
        full_name = "{} {}".format(self.first_name, self.last_name)
        return full_name

    def get_absolute_url(self):
        return reverse('keys:person-detail', args=[str(self.id)])

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def paid_deposit(self):
        """
        Check if the person model has an related field 'deposit',
        if yes return True if not False.
        """
        if hasattr(self, 'deposits'):
            if self.deposits.active():
                return True
        else:
            return False

    def get_active_deposit(self):
        """
        Check if the person model has an related field 'deposit',
        if yes make sure there's only one active at the moment,
        then get the object out of the queryset amd return it.
        """
        if hasattr(self, 'deposits'):
            deposits = self.deposits.active()
            # check if empty
            if len(deposits) == 0:
                return None

            elif len(deposits) == 1:
                deposit = deposits.get()
                return deposit

            else:
                logging.error("Person has {} active deposit: {}".format(len(deposits), deposits))
                raise ValueError("Person has more than one active deposit")
        else:
            return None


    def get_active_issues(self):
        return self.issues.active()

    def get_active_issues_today(self):
        return self.issues.active_today()

    def get_active_issues_earlier(self):
        return self.issues.active_earlier()

    def get_inactive_issues(self):
        return self.issues.inactive()

    def get_inactive_issues_today(self):
        return self.issues.inactive_today()

    def get_inactive_issues_earlier(self):
        return self.issues.inactive_earlier()


    # Tell django-admin to display this as an Boolian
    paid_deposit.boolean = True
    paid_deposit.short_description = "Kaution"



class Deposit(models.Model):
    id = HashidAutoField(primary_key=True)

    state_choices = [('in', 'Eingezahlt'),
                     ('retained', 'Einbehalten'),
                     ('out', 'Ausgezahlt')]

    currency_choices = [('EUR', '€')]

    method_choices = [('cash', 'Bar'),
                      ('bank_transfer', 'Überweisung')]

    state = models.CharField('Status', max_length=8, choices=state_choices, default='in')
    person = models.ForeignKey('Person', related_name='deposits', verbose_name='Person', on_delete=models.CASCADE)
    amount = models.DecimalField('Betrag', max_digits=5, decimal_places=2, default=50,
                                           validators=[amount_is_not_negative_and_reasonable], blank=True)
    currency = models.CharField('Währung', max_length=3, choices=currency_choices, default='EUR')
    comment = models.CharField('Kommentar', max_length=500, null=True, blank=True, validators=[NoControlCharactersValidator, NoWhitespaceValidator])

    in_datetime = models.DateTimeField('Einzahlungszeitpunkt', default=timezone.now,
                                                               validators=[present_or_max_3_days_ago])
    in_method = models.CharField('Einzahlungsmittel', max_length=64, choices=method_choices, default='cash')

    retained_datetime = models.DateTimeField('Einbehaltungszeitpunkt', null=True,
                                                                       validators=[present_or_max_3_days_ago])
    out_datetime = models.DateTimeField('Rückzahlungszeitpunkt', null=True,
                                                                 validators=[present_or_max_3_days_ago])
    out_method = models.CharField('Auszahlungsmittel', max_length=64, choices=method_choices, null=True)

    history = HistoricalRecords()


    created_at = models.DateTimeField('Erstellungszeitpunkt', auto_now_add=True)
    updated_at = models.DateTimeField('Aktualisierungszeitpunkt', auto_now=True)


    objects = DepositManager()

    class Meta:
        verbose_name = "Kaution"
        verbose_name_plural = "Kautionen"
        ordering = ["in_datetime", "amount"]

        constraints = [
            models.CheckConstraint(
                # Make sure that the data attached to each state is consistend
                name='state_consistancy',
                check=models.Q(state='in', out_datetime__isnull=True,
                                           out_method__isnull=True,
                                           retained_datetime__isnull=True) | \
                      models.Q(state='retained', out_datetime__isnull=True,
                                                 out_method__isnull=True,
                                                 retained_datetime__isnull=False) | \
                      models.Q(state='out', out_datetime__isnull=False,
                                            out_method__isnull=False)
            ),
            models.UniqueConstraint(
                name='only_one_active_deposit',
                fields=['person'],
                condition=models.Q(state='in'),
            ),
            models.CheckConstraint(
                name='take_in_deposit_before_give_out',
                check=models.Q(in_datetime__lte=models.F('out_datetime')),
            ),
            models.CheckConstraint(
                name='deposit_not_negative',
                check=models.Q(amount__gte=0),
            )
        ]

    def __str__(self):
        full_name = "{}\xa0{} von\xa0{}".format(self.amount, self.currency, self.person.get_full_name())
        return full_name

    # Django makes it unneccecary hard to acces verbose name from template.
    def get_in_method(self):
        if self.in_method == 'cash':
            return 'in Bar'
        elif self.in_method == 'bank_transfer':
            return 'durch Überweisung'

    def get_out_method(self):
        if self.out_method == 'cash':
            return 'in Bar'
        elif self.out_method == 'bank_transfer':
            return 'durch Überweisung'

    def get_state(self):
        if self.state == 'in':
            return 'eingezahlt'
        elif self.state == 'retained':
            return 'einbehalten'
        elif self.state == 'out':
            return 'ausgezahlt'

    def get_absolute_url(self):
        return reverse('keys:deposit-detail', kwargs={'pk_p': self.person.id, 'pk_d': self.id })




class Issue(models.Model):
    active = models.BooleanField(verbose_name='Aktiv', default=True)
    person = models.ForeignKey('Person',
                               related_name="issues",
                               verbose_name='Person',
                               on_delete=models.CASCADE)

    key = models.ForeignKey('Key', related_name="issues",
                            verbose_name='Schlüssel',
                            on_delete=models.PROTECT)
                            # limit_choices_to= models.Q(issues__active=True, stolen_or_lost=True)
                            # BUG in django: https://code.djangoproject.com/ticket/11707
                            # Workadround: overwritten __init__ of IssueForm.

    out_date = models.DateField('Ausgabedatum',
                                default=timezone.now,
                                validators=[present_or_past_date])
    in_date = models.DateField('Rückgabedatum',
                                null=True, blank=True,
                                validators=[present_or_max_10_days_ago])
    comment = models.CharField('Kommentar', max_length=500, null=True, blank=True, validators=[NoControlCharactersValidator, NoWhitespaceValidator])

    created_at = models.DateTimeField('Erstellungszeitpunkt', auto_now_add=True)
    updated_at = models.DateTimeField('Aktualisierungszeitpunkt', auto_now=True)

    history = HistoricalRecords()

    objects = IssueManager()

    id = HashidAutoField(primary_key=True)

    class Meta:
        verbose_name='Ausleihe'
        verbose_name_plural='Ausleihen'
        ordering = ['-out_date', '-in_date', 'updated_at']

        constraints = [
            models.UniqueConstraint(
                name='key_not_yet_returned',
                fields=['key'],
                condition=models.Q(active=True),
            ),
            models.CheckConstraint(
                # make sure the state is consistend with regards to the indate.
                # only inactive Issues may have a in_datetime.
                name='active_issue_no_in_date',
                check=models.Q(active=True, in_date__isnull=True) | \
                      models.Q(active=False, in_date__isnull=False)
            ),
            models.CheckConstraint(
                name='give_out_key_before_take_in',
                check=models.Q(out_date__lte=models.F('in_date')),
            ),
        ]

    def __str__(self):
        return "{} an\xa0{}".format(self.key, self.person)

    def get_absolute_url(self):
        return reverse('keys:issue-detail', args=[str(self.id)])


