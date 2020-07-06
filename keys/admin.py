from django.contrib import admin

from .models import *

admin.site.site_header = "Schlüsselverwaltungssystem"

class DoorInline(admin.TabularInline):
    model = Door
    extra = 0



@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    def get_locking_system(self, obj):
        return obj.room.locking_system_door

    list_display = ('full_name', 'identifier')
    list_filter = ('building', 'group', 'purpose' )

    inlines = [DoorInline]



@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    #List
    list_display = ('identifier', 'name', 'get_number_of_rooms')


@admin.register(Door)
class DoorAdmin(admin.ModelAdmin):
    def get_building(self, obj):
        return obj.room.building.identifier

    def get_discription(self, obj):
        if obj.kind == 'access':
            if obj.room.name:
                return "Zugangstür zum {} ({})".format(obj.room.name, obj.room.number)
            else:
                return "Zugangstür zu {}{}".format(obj.room.name, obj.room.number)
        else:
            if obj.room.name:
                return "Verbindungstür zum {} ({})".format(obj.room.name, obj.room.number)
            else:
                return "Verbindungstür zu {}{}".format(obj.room.name, obj.room.number)

    get_building.short_description = "Gebäude"
    get_discription.short_description = "Bescheibung"

    # List
    list_display = ('get_discription', 'get_building', 'comment', 'active')
    list_display_links = ['get_discription']

    list_editable = ['active']
    list_filter = ('room__building', 'kind', 'locking_system_door__method')
    list_select_related = ['room__building'] #smaller sql querry



@admin.register(Key)
class KeyAdmin(admin.ModelAdmin):
    def get_kind(self, obj):
        return obj.locking_system_key.kind

    get_kind.short_description = 'Typ'

    # List
    list_display = ('number', 'get_kind')
    list_filter = ('storage_location', 'locking_system_key__method', 'created_at')
    list_select_related = ['locking_system_key'] #smaller sql query



@admin.register(LockingSystem)
class LockingSystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'method', 'comment')

    list_filter = ['method']




@admin.register(StorageLocation)
class StorageLocationAdmin(admin.ModelAdmin):

    def get_location(self, obj):
        return obj.location

    get_location.short_description = "Raum"

    list_display = ('name', 'get_location', 'get_number_of_keys')
    list_filter = [('location__name')]






@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'university_email', 'private_email', 'phone_number', 'deposit_paid')
    list_filter = ('group', 'deposit_paid', 'updated_at')
    search_fields = ['first_name', 'family_name']

    list_editable = ['deposit_paid']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name']

