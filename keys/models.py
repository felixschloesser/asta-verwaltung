from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime

# Create your models here.
class Building(models.Model):
    identifier = models.CharField('Gebäude', max_length=8, unique=True) # not NULL
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


class Room(models.Model):
    building = models.ForeignKey('building', verbose_name='Gebäude',
                                  on_delete=models.CASCADE)
    number = models.CharField("Raumnummer", max_length=32)
    group = models.ForeignKey('group', verbose_name='Gruppe',
                               on_delete=models.PROTECT)
    name = models.CharField('Raumname', max_length=32, unique=True, blank=True, null=True)


    purpose_choices = [('committee', 'Gremienraum'),
                       ('office', 'Büroraum'),
                       ('seminar', 'Seminarraum'),
                       ('storage', 'Lager'),
                       ('event location', 'Veranstaltungslocation'),
                       ('multipurpose', 'Mehrzweckraum'),
                       ('hallway', 'Flur'),
                       ('other', 'Anderer')]
    purpose = models.CharField('Zweck', max_length=32, choices=purpose_choices)
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
            return "{}{}".format(self.building,self.number)

    def identifier(self):
        return "{}{}".format(self.building, self.number)

    def full_name(self):
        return "{} {}".format(self.group, self.name)

    identifier.short_description = "Raumnummer"
    full_name.short_description = "Name"


class Door(models.Model):
    active = models.BooleanField("Aktiv", default=True)
    room = models.ForeignKey("Room", verbose_name="führt in Raum",
                             on_delete=models.CASCADE)
    kind_choices = [('access', 'Zugangstüre'),
                    ('connecting', 'Verbindungstür')]
    kind = models.CharField('Typ', max_length=32, choices=kind_choices,
                             default=('access', 'Zugangstüre'))
    locking_system_door = models.ForeignKey('lockingSystem',
                                             related_name='locking_system_door',
                                             verbose_name='Schließsystem',
                                             on_delete = models.CASCADE)
    comment = models.CharField("Kommentar",max_length=64, blank=True)
    created_at = models.DateTimeField('Erstellungszeitpunkt', auto_now_add=True)
    updated_at = models.DateTimeField('Aktualisierungszeitpunkt', auto_now=True)

    class Meta:
        verbose_name = "Tür"
        verbose_name_plural = "Türen"



class Key(models.Model):
    number = models.CharField("Schlüsselnummer", max_length=32)
    doors = models.ManyToManyField("Door")
    locking_system_key = models.ForeignKey('lockingSystem',
                                            related_name='locking_system_key',
                                            verbose_name='Schließsystem',
                                            on_delete = models.CASCADE)
    storage_location = models.ForeignKey('StorageLocation',
                                          verbose_name='Aufbewahrungsort',
                                          on_delete=models.PROTECT)

    created_at = models.DateTimeField('Erstellungszeitpunkt', auto_now_add=True)
    updated_at = models.DateTimeField('Aktualisierungszeitpunkt', auto_now=True)

    class Meta:
        verbose_name = "Schlüssel"
        verbose_name_plural = "Schlüssel"

        constraints = [
            models.UniqueConstraint(fields=['number', 'locking_system_key'],
                                    name='key_number+locking_system_is_unique')
    ]


    # if not rented -> require location, key-safe?
    def __str__(self):
        return self.number





class StorageLocation(models.Model):
    name = models.CharField("Name", max_length=32)
    location = models.ForeignKey("Room", verbose_name='Ort', on_delete=models.CASCADE)
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



class Person(models.Model): # Add a chron job ro delete after a 2 years of not renting?
    first_name = models.CharField('Vorname', max_length=64)
    family_name = models.CharField('Familienname', max_length=64)
    university_email = models.EmailField('Uni-Mail', unique=True)
    private_email = models.EmailField('Private Mail', unique=True)
    phone_number = PhoneNumberField('Telefon', unique=True)
    group = models.ForeignKey('Group', verbose_name='Gruppe', on_delete=models.PROTECT, blank=True, null=True)
    created_at = models.DateTimeField('Erstellungszeitpunkt', auto_now_add=True)
    updated_at = models.DateTimeField('Aktualisierungszeitpunkt', auto_now=True)

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "Personen"
        ordering = ['family_name', 'first_name']


        constraints = [
            models.UniqueConstraint(fields=['first_name', 'family_name'], name='first_name+family_name_is_unique')
        ]

    def __str__(self):
        return "{} {}".format(self.first_name, self.family_name)



class Group(models.Model):
    name = models.CharField('Name', max_length=64, unique=True)
    created_at = models.DateTimeField('Erstellungszeitpunkt', auto_now_add=True)
    updated_at = models.DateTimeField('Aktualisierungszeitpunkt', auto_now=True)

    class Meta:
        verbose_name = "Gruppe"
        verbose_name_plural = "Gruppen"
        ordering = ['name']


    def __str__(self):
        return "{}".format(self.name)
