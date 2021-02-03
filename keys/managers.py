from django.db import models

class GroupManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.prefetch_related('person', 'group')



class BuildingManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs

class DoorManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('room')

    def access(self):
        self.filter(kind__exact='access')


class RoomManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('building', 'purpose', 'group')

    def of_group(self, name):
        return self.filter(group__name__iexact=name)

    def of_fsr(self):
        return self.filter(group_name_icontains='fsr')

    def of_students(self):
        return self.union(self.of_group('asta'), self.of_group('stupa'), self.of_fsr())

    def accessible_by(self, key_id):
        return self.filter(doors__keys__id__exact=key_id).distinct()


class KeyManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('locking_system').prefetch_related('issues')

    # Returning QuerrySets
    def stolen_or_lost(self, *args, **kwargs):
        return self.filter(stolen_or_lost=True).filter(*args, **kwargs)

    def not_stolen_or_lost(self, *args, **kwargs):
        return self.exclude(stolen_or_lost=True).filter(*args, **kwargs)

    def currently_issued(self, *args, **kwargs):
        return self.filter(issues__active=True).filter(*args, **kwargs).distinct()

    def not_currently_issued(self, *args, **kwargs):
        return self.exclude(issues__active=True).filter(*args, **kwargs).distinct()


    def availible(self):
        availible = self.intersection(self.not_stolen_or_lost(), self.not_currently_issued())
        return availible

    # Not Returning QuerrySets
    def stolen_or_lost_percent(self):
        percent = self.stolen_or_lost().count() / self.count() * 100
        return int(percent)

    def currently_issued_percent(self):
        percent = self.currently_issued().count() / self.count() * 100
        return int(percent)

    def availible_percent(self):
        percent = self.availible().count() / self.count() * 100
        return int(percent)



class PersonManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('group').prefetch_related('issues')

    # Returning QuerrySets
    def paid_deposit(self, *args, **kwargs):
        return self.filter(deposits__state__exact='in').filter(*args, **kwargs)

    def not_paid_deposit(self, *args, **kwargs):
        return self.exclude(deposits__state__exact='in').filter(*args, **kwargs)


    def active_issues(self, *args, **kwargs):
        return self.filter(issues__active__exact=True).distinct().filter(*args, **kwargs)

    def no_active_issues(self, id, *args, **kwargs):
        return self.exclude(issues__active__exact=True).distinct().filter(*args, **kwargs) # double check!
    

    def of_group(self, name):
        return self.filter(group__name__exact=name)


    # Not Returning QuerrySets
    def paid_deposit_percent(self):
        percent = self.paid_deposit().count() / self.count() * 100
        return int(percent)

    def active_issues_percent(self):
        percent = self.active_issues().count() / self.count() * 100
        return int(percent)

    def get_person(self, id):
        return self.filter(id__exact=id).get()



class DepositManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('person')


    def active(self, *args, **kwargs):
        # the method accepts **kwargs, so that it is possible to filter
        # active issues
        # i.e: Issue.all_issues.active(insertion_date__gte=datetime.now)
        return self.filter(state='in', *args, **kwargs)




class IssueManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('person', 'key', 'key__locking_system')

    def active(self, *args, **kwargs):
        # the method accepts **kwargs, so that it is possible to filter
        # active issues
        # i.e: Issue.all_issues.active(insertion_date__gte=datetime.now)
        return self.filter(active=True, *args, **kwargs)

    # Not returning QuerySet
    def active_percent(self):
        percent = self.active().count() / self.count() * 100
        return int(percent)




