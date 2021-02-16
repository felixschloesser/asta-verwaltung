from django.contrib import admin
from django.utils.text import slugify
from django.http import HttpResponse
from django import forms

import csv

from simple_history.admin import SimpleHistoryAdmin
from django.contrib.admin import widgets

from .models import *
admin.site.site_header = "Administration"

# Actions
class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Ausgewählte als CSV exportieren"


# Mixins
class HashIdFieldAdminMixin:
    def _decode_id(self, model, object_id):
        decoded_id = str(model(id=0).id.decode(object_id))

        return decoded_id

    def history_view(self, request, object_id, extra_context=None):
        decoded_id = self._decode_id(self.model, object_id)

        return super().history_view(request, decoded_id, extra_context=extra_context)

    def history_form_view(self, request, object_id, version_id):
        decoded_id = self._decode_id(self.model, object_id)

        return super().history_form_view(request, decoded_id, version_id)



# Inlines
class DoorInline(admin.TabularInline):
    model = Door
    extra = 0


class DepositInline(admin.TabularInline):
    model = Deposit
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["state", "amount", 'currency', 'in_datetime', 'in_method', 'retained_datetime', 'out_datetime', 'out_method', 'comment']
        else:
            return []

# Model Admins
@admin.register(Purpose)
class PuropseAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False

    list_display = ['name']
 



@admin.register(Room)
class RoomAdmin(admin.ModelAdmin, ExportCsvMixin):

    def get_locking_system(self, obj):
        return obj.room.locking_system

    list_display = ('__str__', 'get_identifier')
    list_filter = ('building', 'group', 'purpose' )

    inlines = [DoorInline]
    actions = ["export_as_csv"]


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin, ExportCsvMixin):
    #List
    list_display = ('identifier', 'name', 'get_number_of_rooms')
    actions = ["export_as_csv"]


@admin.register(Door)
class DoorAdmin(admin.ModelAdmin, ExportCsvMixin):

    def has_module_permission(self, request):
        return False

    def get_building(self, obj):
        return obj.room.building.identifier

    get_building.short_description = "Gebäude"

    # List
    list_display = ('__str__', 'get_building', 'comment', 'active')
    list_display_links = ['__str__']

    list_editable = ['active']
    list_filter = ('room__building', 'kind', 'locking_system__method')
    list_select_related = ['room__building'] #smaller sql querry
    actions = ["export_as_csv"]


@admin.register(Key)
class KeyAdmin(admin.ModelAdmin, ExportCsvMixin):
    # List
    list_display = ('number', 'locking_system', 'get_number_of_doors', 'is_currently_issued')
    list_filter = ('stolen_or_lost', 'storage_location', 'locking_system__method', 'created_at')
    list_select_related = ['locking_system'] #smaller sql query
    actions = ["export_as_csv"]

    search_fields = ['number', 'locking_system__name']

    def get_search_results(self, request, queryset, search_term):
        queryset=Key.all_keys.not_currently_issued(stolen_or_lost=False)
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        return queryset, use_distinct

@admin.register(LockingSystem)
class LockingSystemAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ('name', 'company', 'method', 'comment')

    list_filter = ['method']
    actions = ["export_as_csv"]


@admin.register(StorageLocation)
class StorageLocationAdmin(admin.ModelAdmin, ExportCsvMixin):

    def get_location(self, obj):
        return obj.location

    get_location.short_description = "Raum"

    list_display = ('name', 'get_location', "get_number_of_keys")
    list_filter = [('location__name')]
    actions = ["export_as_csv"]


@admin.register(Person)
class PersonAdmin(HashIdFieldAdminMixin, admin.ModelAdmin, ExportCsvMixin):
    list_display = ('__str__', 'university_email', 'private_email', 'phone_number', 'paid_deposit')
    list_filter = ('group', 'deposits__amount', 'updated_at')
    search_fields = ['first_name', 'last_name']

    inlines = [DepositInline]
    actions = ["export_as_csv"]


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ['name']

    def has_module_permission(self, request):
        return False



@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin, ExportCsvMixin):
    autocomplete_fields = ['person', 'key']

    date_hierarchy = 'updated_at'
    list_display = ['person', 'key', 'comment', 'out_date', 'in_date']
    list_filter = ['active', 'out_date', 'updated_at']
    
    search_fields = ['person__first_name', 'person__last_name', 'key__number']
    actions = ["export_as_csv"]





# admin.site.register(Deposit, SimpleHistoryAdmin)
# Waiting for fix: admin.site.register(Person, SimpleHistoryAdmin)
# admin.site.register(StorageLocation, SimpleHistoryAdmin)
# admin.site.register(LockingSystem, SimpleHistoryAdmin)
# admin.site.register(Key, SimpleHistoryAdmin)
# admin.site.register(Door, SimpleHistoryAdmin)
# admin.site.register(Group, SimpleHistoryAdmin)
# admin.site.register(Building, SimpleHistoryAdmin)
# admin.site.register(Room, SimpleHistoryAdmin)
# admin.site.register(Purpose, SimpleHistoryAdmin)

