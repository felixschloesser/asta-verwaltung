from django.contrib import admin

from .models import *
admin.site.site_header = "Administration"

class DoorInline(admin.TabularInline):
    model = Door
    extra = 0


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    def get_locking_system(self, obj):
        return obj.room.locking_system

    list_display = ('__str__', 'get_identifier')
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

    get_building.short_description = "Gebäude"

    # List
    list_display = ('__str__', 'get_building', 'comment', 'active')
    list_display_links = ['__str__']

    list_editable = ['active']
    list_filter = ('room__building', 'kind', 'locking_system__method')
    list_select_related = ['room__building'] #smaller sql querry



@admin.register(Key)
class KeyAdmin(admin.ModelAdmin):
    # List
    list_display = ('number', 'locking_system', 'get_number_of_doors')
    list_filter = ('stolen_or_lost', 'storage_location', 'locking_system__method', 'created_at')
    list_select_related = ['locking_system'] #smaller sql query



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
    list_display = ('__str__', 'university_email', 'private_email', 'phone_number', 'has_paid_deposit')
    list_filter = ('group', 'deposit__amount', 'updated_at')
    search_fields = ['first_name', 'last_name']


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ('person', 'amount', 'in_datetime', 'out_datetime')
    list_filter = ('amount', 'in_method', 'out_datetime')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ['person', 'key', 'out_date', 'updated_at']
    list_filter = ['out_date', 'updated_at']

    search_fields = ['person__first_name', 'person__last_name', 'key__number']





