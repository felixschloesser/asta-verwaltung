from import_export import resources, fields, widgets

from .models import Key, Person, Group

# Import / Export Ressources
class KeyResource(resources.ModelResource):

    
    class Meta:
        model = Key



class PersonResource(resources.ModelResource):
    first_name = fields.Field(attribute='first_name', column_name='Vorname')
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
