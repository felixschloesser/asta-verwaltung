from django.db import models

# Create your models here.
class Building(models.Model):
    identifier = models.CharField("Identifier", max_length=8, unique=True) # not NULL


class Room(models.Model):
    number = models.CharField("Room number",max_length=32)
    building = models.ForeignKey('Building', on_delete = models.CASCADE)

    class Meta:
        models.UniqueConstraint(fields=['building', 'number'], name='room_is_unique')


class Door(models.Model):
    room = models.ForeignKey('Room', on_delete = models.CASCADE)
    comment = models.CharField(max_length=64, blank=True)


class Key(models.Model):
    number = models.CharField("Key number", max_length=32)
    doors = models.ManyToManyField("Door")
    locking_system = models.ForeignKey('LockingSystem', on_delete = models.CASCADE)
# if not rentent -> require location, key-safe?

class LockingSystem(models.Model):
    name = models.CharField("Name", max_length=32, unique=True)
    kind = [('mechanical', 'Mechanical'),
            ('mechatronical', 'Mechatronical'),
            ('transponder', 'Transponder')]
    company = models.CharField(max_length=32, unique=True)

    class Meta:
        models.UniqueConstraint(fields=['name', 'company'], name='locking_system_is_unique')
# Persons
#EmailField


# Groups
