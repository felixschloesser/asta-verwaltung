from import_export import resources, fields, widgets

from .models import Key, Issue ,Person, Group, Door, LockingSystem, StorageLocation

# Import / Export Ressources
class KeyResource(resources.ModelResource):
    number = fields.Field(attribute='number', column_name='Schlüsselnummer')
    doors = fields.Field(attribute='doors', column_name='Türen',
                         widget=widgets.ManyToManyWidget(Door))
    locking_system = fields.Field(attribute='locking_system', column_name='Schließsystem',
                                    widget=widgets.ForeignKeyWidget(LockingSystem))
    storage_location = fields.Field(attribute='storage_location', column_name='Aufbewahrungsort',
                                    widget=widgets.ForeignKeyWidget(StorageLocation))
    stolen_or_lost = fields.Field(attribute='stolen_or_lost', column_name='Gestohlen/Verloren',
                                    widget=widgets.BooleanWidget())
    comment = fields.Field(attribute='comment', column_name='Kommentar')
    created_at = fields.Field(attribute='created_at',
                              column_name='Erstellungszeitpunkt',
                              widget=widgets.DateTimeWidget())
 
    class Meta:
        model = Key
        exclude = ['updated_at']

    def dehydrate_doors(self, key):
        doorList = []
        for door in key.doors.all():
            doorList.append(str(door))

        return ', '.join(map(str, doorList))


    def dehydrate_locking_system(self, key):
        return str(key.locking_system)

    def dehydrate_storage_location(self, key):
        return str(key.storage_location)

    def get_queryset(self):
        return self._meta.model.objects.all()


class IssueResource(resources.ModelResource):
    active = fields.Field(attribute='active', column_name='Aktiv',
                                    widget=widgets.BooleanWidget())
    person = fields.Field(attribute='person', column_name='Person',
                         widget=widgets.ForeignKeyWidget(Person))
    key = fields.Field(attribute='key', column_name='Schlüssel',
                                    widget=widgets.ForeignKeyWidget(Key))
    out_date = fields.Field(attribute='out_date', column_name='Ausgabedatum',
                                    widget=widgets.DateWidget())
    in_date = fields.Field(attribute='in_date', column_name='Rückgabedatum',
                                    widget=widgets.DateWidget())
    comment = fields.Field(attribute='comment', column_name='Kommentar')

    created_at = fields.Field(attribute='created_at',
                              column_name='Erstellungszeitpunkt',
                              widget=widgets.DateTimeWidget())
 
    class Meta:
        model = Issue
        exclude = ['updated_at']

    def dehydrate_person(self, issue):
        return str(issue.person)

    def dehydrate_key(self, issue):
        return str(issue.key)

    def get_queryset(self):
        return self._meta.model.objects.all()


class PersonResource(resources.ModelResource):
    first_name = fields.Field(attribute='first_name', column_name='Vorname')
    last_name = fields.Field(attribute='last_name', column_name='Nachname')
    university_email = fields.Field(attribute='university_email', column_name='Uni Mail')
    private_email = fields.Field(attribute='private_email', column_name='Private Mail')
    phone_number = fields.Field(attribute='phone_number', column_name='Telefon')
    group = fields.Field(attribute='group',
                         column_name='Gruppe',
                         widget=widgets.ForeignKeyWidget(Group, 'name'))
    created_at = fields.Field(attribute='created_at',
                              column_name='Erstellungszeitpunkt',
                              widget=widgets.DateTimeWidget())


    class Meta:
        model = Person
        exclude = ['updated_at']

    def dehydrate_id(self, person):
        try:
            id = person.id.id
        except AttributeError:
            id = ""

        return id

    def get_queryset(self):
        return self._meta.model.objects.all()
