from django.shortcuts import render, get_object_or_404
from django.views import View, generic
from django.db import models
from django.urls import reverse_lazy
from django.http import Http404
from django.utils import timezone

from django.core.exceptions import ValidationError

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from .models import *
from .forms import *

import datetime
import logging

import os

def index_view(request):
    return render(request, 'keys/index.html')


class Home(generic.ListView):
    queryset = Issue.objects.active()
    ordering = ['-updated_at']
    paginate_by = 5
    context_object_name = 'issues'
    template_name = 'keys/home.html'

    def get_context_data(self, **kwargs):
        """
        Add all people, all keys and all rooms to the view so we can display statisics
        """
        context = super().get_context_data(**kwargs)
        context["people"] = Person.objects
        context["keys"] = Key.objects
        context["rooms"] = Room.objects

        return context



# Keys
class KeyListAll(LoginRequiredMixin, generic.ListView):
    model = Key
    paginate_by = 20
    template_name_suffix = '_list_all'


class KeyListIssued(LoginRequiredMixin, generic.ListView):
    queryset = Key.objects.currently_issued()
    paginate_by = 20
    template_name_suffix = '_list_issued'


class KeyListLost(LoginRequiredMixin, generic.ListView):
    queryset = Key.objects.stolen_or_lost()
    paginate_by = 20
    template_name_suffix = '_list_lost'



class KeySearchResults(LoginRequiredMixin, generic.ListView):
    model = Key
    template_name_suffix = '_search_results'

    def get_queryset(self):
        # Alter the queryset of the list view, so that it only contains the entries
        # of the keys where matching the search query in the get request
        storage_location_query_parameter = self.request.GET.get('storage_location')
        if storage_location_query_parameter:
            key_list = Key.objects.filter(storage_location__name__icontains=storage_location_query_parameter)

            return key_list

        search_query_parameter = self.request.GET.get('q')
        if search_query_parameter:
            key_list = Key.objects.filter(models.Q(number__startswith=search_query_parameter) |
                                           models.Q(locking_system__name__icontains=search_query_parameter) |
                                           models.Q(locking_system__company__icontains=search_query_parameter)
                                          )
        else:
            key_list = Key.objects.none()
        return key_list



class KeyDetail(LoginRequiredMixin, generic.DetailView):
    model = Key



class KeyLost(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    model = Key
    form_class = KeyLostForm
    template_name_suffix ='_lost'
    success_message = "Als gestolen/verloren gemeldet."
    widgets = {
            'comment': forms.Textarea(attrs={'cols': 80,
                                             'rows': 3,
                                             'placeholder': "Optionaler Kommentar zur Entgegennahme...",
                                             'spellcheck': 'true',
                                             'lang': 'de-DE'}),
        }

    def form_valid(self, form):
        """
        Before validating the form, set the stolen_or_lost field to True
        so that this view actually does what it name says it does.
        """
        self.object = form.save(commit=False)
        self.object.stolen_or_lost = True
        self.object.save()

        logging.info('Lost key: {}'.format(self.object))
        return super().form_valid(form)

    def get_success_url(self):
        issue = self.object.get_current_issue()
        logging.debug(issue)
        if issue:
            return reverse_lazy('keys:person-detail',  args=[issue.person.id])
        else:
            return reverse_lazy('keys:key-detail',  args=[self.object.id])



class KeyFound(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    model = Key
    form_class = KeyFoundForm
    template_name_suffix ='_found'
    success_message = "Nicht mehr als gestolen/verloren gemeldet."
    widgets = {
            'comment': forms.Textarea(attrs={'cols': 80,
                                             'rows': 3,
                                             'placeholder': "Optionaler Kommentar zur Entgegennahme...", 
                                             'spellcheck': 'true',
                                             'lang': 'de-DE'}),
        }

    def form_valid(self, form):
        """
        Before validating the form, set the stolen_or_lost field to False
        so that this view actually does what it name says it does.
        """
        self.object = form.save(commit=False)
        self.object.stolen_or_lost = False
        self.object.save()
        logging.info('Found key: {}'.format(self.object))
        return super().form_valid(form)



# People
class PersonList(LoginRequiredMixin, generic.ListView):
    context_object_name = 'people'
    queryset = Person.objects.order_by('created_at').reverse()
    paginate_by = 30


class PersonListGroup(LoginRequiredMixin, generic.ListView):
    model = Group
    template_name = 'keys/person_list_group.html'



class PersonSearchResults(LoginRequiredMixin, generic.ListView):
    model = Person
    paginate_by = 30
    template_name_suffix = '_search_results'

    def get_queryset(self):
        # Alter the queryset of the list view, so that it only contains the entries
        # of the people where first or last name of a person match the search query
        # in the get request

        # Start with all people
        person_list = Person.objects.all()


        group_query_parameter = self.request.GET.get('group')
        if group_query_parameter == 'FSR':
            person_list = person_list & Person.objects.of_fsr()

        if group_query_parameter:
            person_list = person_list & Person.objects.of_group(group_query_parameter)

        search_query_parameter = self.request.GET.get('q')
        if search_query_parameter:
            person_list = person_list & Person.objects.filter(models.Q(first_name__istartswith=search_query_parameter) |
                                                              models.Q(last_name__istartswith=search_query_parameter) |
                                                              models.Q(university_email__icontains=search_query_parameter) |
                                                              models.Q(group__name__istartswith=search_query_parameter)
                                                             )

        return person_list



class PersonCreate(SuccessMessageMixin, LoginRequiredMixin, generic.CreateView):
    model = Person
    form_class = PersonForm
    success_message = "%(first_name)s %(last_name)s erfolgreich hinzugefügt."

    def form_valid(self, form):
        """
        Before validating the form, set set the email adress to lowercase
        """
        self.object = form.save(commit=False)
        self.object.university_email = self.object.university_email.lower()
        self.object.private_email = self.object.private_email.lower()
        self.object.save()

        logging.info("Created new Person: {}".format(self.object))

        return super().form_valid(form)



class PersonDetail(LoginRequiredMixin, generic.DetailView):
    model = Person

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        keys = Key.objects
        context["keys"] = keys
        return context



class PersonUpdate(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    model = Person
    form_class = PersonForm
    template_name_suffix = '_update_form'
    success_message = "%(first_name)s %(last_name)s erfolgreich aktualisiert."

    def form_valid(self, form):
        """
        Only here for Logging CRUD actions
        """
        self.object = form.save(commit=False)
        logging.info('Updated Person: {}'.format(self.object))
        return super().form_valid(form)



#  Deposit

class DepositMixin:
    def get_success_url(self):
        return reverse_lazy('keys:person-detail',  args=[self.object.person.id])



class DepositDetail(DepositMixin, LoginRequiredMixin, generic.DetailView):
    model = Deposit
    pk_url_kwarg = 'pk_d'



class DepositCreate(DepositMixin, SuccessMessageMixin, LoginRequiredMixin, generic.CreateView):
    model = Deposit
    form_class = DepositCreateForm
    initial = {'in_method': 'cash'}
    success_message = "Kaution von %(amount)s %(currency)s erfolgreich hinzugefügt."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        person = Person.objects.filter(pk=pk).get()
        context["person"] = person
        return context

    def form_valid(self, form):
        """
        Before validating the form, populate the person field using the request primary key as a lookup for
        """
        self.object = form.save(commit=False)
        pk = self.kwargs.get('pk')
        self.object.person = Person.objects.filter(pk=pk).get()
        self.object.in_datetime = timezone.now()
        self.object.save()
        logging.info("Created Deposit: {}".format(self.object))

        logging.debug("Polulated the 'person' field with pk: {}".format(pk))
        logging.debug("Polulated the 'in_datetime' field with {}".format(timezone.now()))
        return super().form_valid(form)



class DepositRetain(DepositMixin, SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    model = Deposit
    pk_url_kwarg = 'pk_d'
    form_class = DepositRetainForm
    template_name_suffix = '_confirm_retain'
    success_message = "Kaution von erfolgreich einbehalten."

    def form_valid(self, form):
        """
        Before validating the form, populate the person field using the request primary key as a lookup for
        """
        self.object = form.save(commit=False)
        self.object.state = 'retained'
        self.object.retained_datetime = timezone.now()
        self.object.save()
        logging.info("Retained Deposit: {}".format(self.object))

        logging.debug("Setting the state to: 'retained'")
        return super().form_valid(form)



class DepositReturn(DepositMixin, SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    model = Deposit
    pk_url_kwarg = 'pk_d'
    form_class = DepositReturnForm
    template_name = 'keys/deposit_return_form.html'
    initial = {'out_method': 'cash'}
    success_message = "Kaution erfolgreich zurückgegeben."

    def form_valid(self, form):
        """
        Before validating the form, set active to False, the amount to 0 and note the out datetime
        """
        self.object = form.save(commit=False)
        self.object.state = 'out'
        self.object.out_datetime = timezone.now()
        self.object.save()
        logging.info("Returned Deposit: {}".format(self.object))
        logging.debug("Setting the state to: 'out'")
        logging.debug("Popluating the out_datetime with the current time: {}".format(datetime.now()))
        return super().form_valid(form)



class DepositDelete(DepositMixin, LoginRequiredMixin, generic.DeleteView):
    model = Deposit
    pk_url_kwarg = 'pk_d'

    def form_valid(self, form):
        """
        Only here for Logging CRUD actions
        """
        self.object = form.save(commit=False)
        logging.info('Deleted Deposit: {}'.format(self.object))
        return super().form_valid(form)


# Rooms

class RoomListBuilding(LoginRequiredMixin, generic.ListView):
    model = Building
    template_name = "keys/room_list_building.html"


class RoomListGroup(LoginRequiredMixin, generic.ListView):
    model = Group
    template_name = "keys/room_list_group.html"


class RoomSearchResults(LoginRequiredMixin, generic.ListView):
    model = Room
    paginate_by = 30
    template_name_suffix = '_search_results'

    def get_queryset(self):
        """
        Alter the queryset of the list view, so that it only contains the entries
        of the rooms match the search query in the get request
        """
        # Creating a empty room list
        room_list = Room.objects.all()
        logging.debug(room_list)


        # Only Search for Rooms inside a specified building
        building_query = self.request.GET.get('building')
        if building_query:
            room_list = room_list & Room.objects.filter(building__identifier__exact=building_query)

        # Only Search for Rooms of the specified group
        group_query = self.request.GET.get('group')

        if group_query == "FSR":
            # All Rooms which belong to a FSR
            room_list = room_list & Room.objects.of_fsr()

        elif group_query:
            room_list = room_list & Room.objects.of_group(group_query)

        # General Search Querys
        search_query = self.request.GET.get('q')
        if search_query:
            room_list = room_list & Room.objects.filter(models.Q(number__icontains=search_query) |
                                            models.Q(name__icontains=search_query) |
                                            models.Q(purpose__name__icontains=search_query) |
                                            models.Q(building__name__istartswith=search_query) |
                                            models.Q(building__identifier__istartswith=search_query) |
                                            models.Q(group__name__istartswith=search_query)
                                           )

        logging.debug(room_list)
        return room_list



class RoomDetail(LoginRequiredMixin, generic.DetailView):
    model = Room

    def get_context_data(self, **kwargs):
        # Add all Issues of keys that have access to this room as a seperate
        # context
        context = super().get_context_data(**kwargs)
        room_slug = self.kwargs.get('slug')
        logging.debug(room_slug)
        relevant_issues = Issue.objects.active().filter(key__doors__room__slug__exact=room_slug,
                                                           key__doors__kind__exact='access'
                                                          )
        context['issues'] = relevant_issues

        return context




# Issues

class IssueListAll(LoginRequiredMixin, generic.ListView):
    model = Issue
    paginate_by = 20
    template_name_suffix ='_list_all'


class IssueListActive(LoginRequiredMixin, generic.ListView):
    queryset = Issue.objects.active()
    paginate_by = 20
    template_name_suffix ='_list_active'



class IssueSearchResults(LoginRequiredMixin, generic.ListView):
    model = Issue
    paginate_by = 20
    template_name_suffix = '_search_results'

    def get_queryset(self):
        # Alter the queryset of the list view, so that it only contains the entries
        # of the Issues where matching the search query in the get request
        query = self.request.GET.get('q','')

        issue_list = Issue.objects.filter(models.Q(person__first_name__icontains=query) |
                                             models.Q(person__last_name__icontains=query) |
                                             models.Q(key__number__startswith=query),
                                            )
        return issue_list



class IssueDetail(LoginRequiredMixin, generic.DetailView):
    model = Issue



class IssueNew(SuccessMessageMixin, LoginRequiredMixin, generic.CreateView):
    model = Issue
    form_class = IssueForm
    success_message = "Ausgabe von %(key)s erfolgreich angelegt."

    def get_context_data(self, **kwargs):
        """
        Get the person from the request and add it to the context
        so that the tempalte can access it.
        """
        context = super().get_context_data(**kwargs)
        person_id = self.kwargs.get('pk')
        person = Person.objects.get_person(person_id)
        context['person'] = person
        return context

    def form_valid(self, form):
        """
        Before validating the form, set active to True and populate the person field using
        the request primary key as a lookup for
        """
        person_id = self.kwargs.get('pk')
        self.object = form.save(commit=False)
        self.object.person = Person.objects.get_person(person_id)
        self.object.active = True
        self.object.save()
        logging.info("New Issue: {}".format(self.object))
        return super().form_valid(form)

    def get_success_url(self):
        if "another" in self.request.POST:
            return reverse_lazy('keys:issue-new', args=[self.object.person.id])
        else:
            return reverse_lazy('keys:person-detail',  args=[self.object.person.id])



class IssueReturn(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    model = Issue
    form_class = IssueReturnForm
    template_name_suffix ='_return_form'

    success_message = "%(key)s erfolgreich zurückgegeben."

    def form_valid(self, form):
        """
        Before validating the form, set active to False
        """
        self.object = form.save(commit=False)
        self.object.active = False
        self.object.save()
        logging.debug("Setting active to 'False'")
        logging.info("Returned Issue: {}".format(self.object))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('keys:person-detail',  args=[self.object.person.id])

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            key=self.object.key,
        )
