from django.db import models

class KeyManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('locking_system')

    def is_availible(self):
        # Is neigher lost or currently rented
        return self.filter(stolen_or_lost=False, issues__in_date__isnull=True)

    def get_number_of_doors(self):
        return self.doors.all().count()

    def get_access_doors(self):
        return self.doors.filter(kind__exact='access')

    def get_current_issue(self):
        issue_set  = self.all_issues.is_active()
        try:
            issue = issue_set.get()
            return issue
        except IndexError:
            return None

    def get_locking_system_method(self):
        return self.locking_system.method

        get_locking_system_method.short_description = 'Typ'
        get_number_of_doors.short_description = "Anzahl Türen"



class PersonManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('group', 'deposit')

    def get_person(self, id,**kwargs):
        return self.filter(id__exact=id).get()

    def get_active_issues(self):
        return self.issues.all_issues.is_active()



class IssueManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('person', 'key')

    def is_active(self, **kwargs):
        # the method accepts **kwargs, so that it is possible to filter
        # active issues
        # i.e: Issue.objects.published(insertion_date__gte=datetime.now)
        return self.filter(in_date__isnull=True, **kwargs)

    is_active.boolean = True
    is_active.short_description = "Aktiv"

