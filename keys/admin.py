from django.contrib import admin

from .models import Building, Room, Door, Key, LockingSystem

class RoomInline(admin.TabularInline):
    model = Room
    extra = 1


class BuildingAdmin(admin.ModelAdmin):
    inlines = [RoomInline]


class KeyAdmin(admin.ModelAdmin):
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "doors":
            kwargs["queryset"] = Car.objects.filter(owner=request.user)
        return super().formfield_for_manytomany(db_field, request, **kwargs)


class DoorAdmin(admin.ModelAdmin):
    # List
    list_display = ('__str__', 'gebäude', 'comment', 'active')
    #list_filter = ['gebäude', 'active', 'comment']

admin.site.register(Building, BuildingAdmin)
admin.site.register(Key, KeyAdmin)
admin.site.register(Door, DoorAdmin)
admin.site.register(LockingSystem)
