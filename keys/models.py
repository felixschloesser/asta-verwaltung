from django.db import models

# Create your models here.
class Building(models.Model):
    identifier = models.CharField(max_length=8, unique=True) # not NULL

    def __str__(self):
        return self.identifier


class Room(models.Model):
    name = models.CharField(max_length=32, unique=True, blank=True)
    number = models.CharField("room number",max_length=32)
    building = models.ForeignKey('building', on_delete = models.CASCADE)
    purpose_choices = [('committee', 'Gremienraum'),
               ('storage', 'Lager'),
               ('learning', 'Lernraum'),
               ('multipurpose', 'Mehrzweckraum'),
               ('other', 'Other')]
    purpose = models.CharField(max_length=32, choices=purpose_choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['building', 'number'], name='room_is_unique')
        ]

    def __str__(self):
        if self.name:
            return self.name
        else:
            return "{}{}".format(self.building,self.number)


class Door(models.Model):
    room = models.ForeignKey("room", on_delete=models.PROTECT)
    active = models.BooleanField("Aktiv", default=True)
    comment = models.CharField(max_length=64, blank=True)

    def __str__(self):
        if self.comment:
            return "zum {} ({})".format(self.room, self.comment)
        else:
            return "zum {}".format(self.room)

    def gebäude(self):
        return self.room.building

class Key(models.Model):
    number = models.CharField("key number", max_length=32)
    doors = models.ManyToManyField("door")
    locking_system = models.ForeignKey('lockingSystem', on_delete = models.CASCADE)
# if not rented -> require location, key-safe?


class LockingSystem(models.Model):
    name = models.CharField(max_length=32, unique=True)
    kind = [('mechanical', 'mechanical key'),
            ('mechatronical', 'mechatronical key'),
            ('transponder', 'transponder')]
    company = models.CharField(max_length=32, unique=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'company'], name='locking_system_is_unique')
        ]

# Persons
#EmailField


# Groups
