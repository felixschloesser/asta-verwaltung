from django.db import models

class KeyManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('locking_system')

    def availible(self, *args, **kwargs):
        # Is either never issued, not lost and not currently rented
        availible =  self.filter(models.Q(stolen_or_lost=False, issues__active=False) |
                                 models.Q(stolen_or_lost=False, issues__isnull=True),
                                 *args, **kwargs).distinct()

        return availible


class PersonManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('group', 'deposit')

    def get_person(self, id, *args, **kwargs):
        return self.filter(id__exact=id, *args, **kwargs).get()


class IssueManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('person', 'key')

    def active(self, *args, **kwargs):
        # the method accepts **kwargs, so that it is possible to filter
        # active issues
        # i.e: Issue.objects.published(insertion_date__gte=datetime.now)
        return self.filter(active=True, *args, **kwargs)
