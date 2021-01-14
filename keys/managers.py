from django.db import models

class KeyManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('locking_system')

    def availible(self, **kwargs):
        # Is neigher lost or currently rented
        return self.filter(stolen_or_lost=False, issues__active=False, **kwargs)





class PersonManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('group', 'deposit')

    def get_person(self, id,**kwargs):
        return self.filter(id__exact=id, **kwargs).get()





class IssueManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('person', 'key')

    def active(self, **kwargs):
        # the method accepts **kwargs, so that it is possible to filter
        # active issues
        # i.e: Issue.objects.published(insertion_date__gte=datetime.now)
        return self.filter(active=True, **kwargs)
