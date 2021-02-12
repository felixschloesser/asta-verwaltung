from django.db import models

class GroupManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs

    def get(self, name):
        return self.filter(name__iexact=name)

    def fsr(self):
        return self.filter(name__icontains='fsr')

    def students(self):
        return self.union(self.get('asta'), self.get('stupa'), self.fsr(), self.get('student'))

    def not_students(self):
        return self.exclude(self.get('asta'), self.get('stupa'), self.fsr(), self.ag() ,self.get('student'))


     # Not Returning QuerrySets
    def fsr_list(self):
        return [ group.name for group in self.fsr()]

    def of_fsr_percent(self):
        if self.count() > 0:
            percent = self.of_fsr().count() / self.count() * 100
            return int(percent)
        else:
            return 0

    def of_ag_percent(self):
        if self.count() > 0:
            percent = self.of_ag().count() / self.count() * 100
            return int(percent)
        else:
            return 0

    def of_students_percent(self):
        if self.count() > 0:
            percent = self.of_students().count() / self.count() * 100
            return int(percent)
        else:
            return 0


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

    def of_asta(self):
        return self.filter(group__name__iexact='asta')

    def of_fsr(self):
        return self.filter(group__name__icontains='fsr')

    def of_ag(self):
        return self.filter(group__name__icontains='ag')

    def of_students(self):
        return self.union(self.of_group('asta'), self.of_group('stupa'), self.of_fsr(), self.of_group('student'))

    def not_students(self):
        return self.exclude(self.of_group('asta'), self.of_group('stupa'), self.of_fsr(), self.of_group('student'))

    def accessible_by(self, key_id):
        return self.filter(doors__keys__id__exact=key_id).distinct()


    # Not Returning QuerrySets
    def of_asta_percent(self):
        if self.count() > 0:
            percent = self.of_asta().count() / self.count() * 100
            return int(percent)
        else:
            return 0

    def of_fsr_percent(self):
        if self.count() > 0:
            percent = self.of_fsr().count() / self.count() * 100
            return int(percent)
        else:
            return 0

    def of_ag_percent(self):
        if self.count() > 0:
            percent = self.of_ag().count() / self.count() * 100
            return int(percent)
        else:
            return 0

    def of_students_percent(self):
        if self.count() > 0:
            percent = self.of_students().count() / self.count() * 100
            return int(percent)
        else:
            return 0

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
        if self.count() > 0:
            percent = self.stolen_or_lost().count() / self.count() * 100
            return int(percent)
        else:
            return 0

    def currently_issued_percent(self):
        if self.count() > 0:
            percent = self.currently_issued().count() / self.count() * 100
            return int(percent)
        else:
            return 0

    def availible_percent(self):
        if self.count() > 0:
            percent = self.availible().count() / self.count() * 100
            return int(percent)
        else:
            return 0


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
        return self.filter(group__name__iexact=name)

    def of_fsr(self):
        return self.filter(group__name__icontains='fsr')

    def of_ag(self):
        return self.filter(group__name__icontains='ag')

    def of_students(self):
        return self.union(self.of_group('asta'), self.of_group('stupa'), self.of_fsr(), self.of_group('student'))

    def not_students(self):
        return self.exclude(self.of_group('asta'), self.of_group('stupa'), self.of_fsr(), self.of_group('student'))

    def accessible_by(self, key_id):
        return self.filter(doors__keys__id__exact=key_id).distinct()



    # Not Returning QuerrySets
    def paid_deposit_percent(self):
        if self.count() > 0:
            percent = self.paid_deposit().count() / self.count() * 100
            return int(percent)
        else:
            return 0

    def active_issues_percent(self):
        if self.count() > 0:
            percent = self.active_issues().count() / self.count() * 100
            return int(percent)
        else:
            return 0

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
        if self.count() > 0:
            percent = self.active().count() / self.count() * 100
            return int(percent)
        else:
            return 0



