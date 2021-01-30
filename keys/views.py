from django.shortcuts import render, get_object_or_404
from django.views import View, generic
from django.db import models
from django.urls import reverse_lazy
from django.http import Http404
from django.utils import timezone

from django.core.exceptions import ValidationError

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from .models import Key, Person, Issue, Deposit, Room, Building
from .forms import *

import datetime
import logging


def index_view(request):
    return render(request, 'keys/index.html')


class Home(generic.ListView):
    queryset = Issue.all_issues.active()
    ordering = ['-updated_at']
    paginate_by = 5
    template_name = 'keys/home.html'


    def get_context_data(self, **kwargs):
        """
        Get the current person from the request and add it to the context so that the tempalte can access it.
        """
        context = super().get_context_data(**kwargs)
        context["people"] = Person.all_people
        context["keys"] = Key.all_keys
        context["rooms"] = Room.all_rooms
        return context



# Keys
class KeyList(LoginRequiredMixin, generic.ListView):
    model = Key
    paginate_by = 20


class KeySearchResults(LoginRequiredMixin, generic.ListView):
    model = Key
    template_name_suffix = '_search_results'

    def get_queryset(self):
        # Alter the queryset of the list view, so that it only contains the entries
        # of the keys where matching the search query in the get request
        query = self.request.GET.get('q')
        if query:
            key_list = Key.all_keys.filter(models.Q(number__startswith=query) |
                                           models.Q(locking_system__name__icontains=query) |
                                           models.Q(locking_system__company__icontains=query)
                                          )
        else:
            key_list = Key.all_keys
        return key_list



class KeyDetail(LoginRequiredMixin, generic.DetailView):
    model = Key



class KeyLost(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    model = Key
    template_name_suffix ='_lost'
    fields = ['stolen_or_lost']
    success_message = "Als gestolen/verloren gemeldet."

    def form_valid(self, form):
        """
        Before validating the form, populate the person field using the request primary key as a lookup for
        """
        self.object = form.save(commit=False)
        self.object.stolen_or_lost = True
        self.object.save()
        return super().form_valid(form)



class KeyFound(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    model = Key
    template_name_suffix ='_found'
    fields = ['stolen_or_lost']
    success_message = "Nicht mehr als gestolen/verloren gemeldet."

    def form_valid(self, form):
        """
        Before validating the form, populate the person field using the request primary key as a lookup for
        """
        self.object = form.save(commit=False)
        self.object.stolen_or_lost = False
        self.object.save()
        return super().form_valid(form)



# People
class PersonList(LoginRequiredMixin, generic.ListView):
    context_object_name = 'people'
    queryset = Person.all_people.order_by('created_at').reverse()
    paginate_by = 30



class PersonSearchResults(LoginRequiredMixin, generic.ListView):
    model = Person
    paginate_by = 30
    template_name_suffix = '_search_results'

    def get_queryset(self):
        # Alter the queryset of the list view, so that it only contains the entries
        # of the people where first or last name of a person match the search query
        # in the get request
        query = self.request.GET.get('q')
        if query:
            person_list = Person.all_people.filter(models.Q(first_name__istartswith=query) |
                                                models.Q(last_name__istartswith=query) |
                                                models.Q(university_email__icontains=query) |
                                                models.Q(group__name__istartswith=query)
                                               )
        else:
            person_list = Person.all_people

        return person_list



class PersonCreate(SuccessMessageMixin, LoginRequiredMixin, generic.CreateView):
    model = Person
    form_class = PersonCreateForm
    success_message = "%(first_name)s %(last_name)s erfolgreich hinzugefügt."



    def form_valid(self, form):
        """
        Before validating the form, set set the email adress to lowercase
        """
        self.object = form.save(commit=False)
        self.object.university_email = self.object.university_email.lower()
        self.object.private_email = self.object.private_email.lower()
        self.object.save()
        return super().form_valid(form)


class PersonDetail(LoginRequiredMixin, generic.DetailView):
    model = Person



class PersonUpdate(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    model = Person
    fields = ['first_name',
              'last_name',
              'university_email',
              'private_email',
              'phone_number',
              'group']
    template_name_suffix = '_update_form'
    success_message = "%(first_name)s %(last_name)s erfolgreich aktualisiert."



#  Deposit
class DepositMixin:
    def get_object(self, queryset=None):
        """
        Get the deposit from the person-pk in the urlpattern.
        """
        queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        obj = queryset.filter(person__id=pk).get()
        return obj

    def get_context_data(self, **kwargs):
        """
        Get the current person from the request and add it to the context so that the tempalte can access it.
        """
        context = super().get_context_data(**kwargs)
        person = Person.all_people.filter(pk=self.kwargs.get('pk')).get()
        context["person"] = person
        return context

    def get_success_url(self):
        return reverse_lazy('keys:person-detail',  args=[self.object.person.id])


class DepositDetail(DepositMixin, LoginRequiredMixin, generic.DetailView):
    model = Deposit



class DepositCreate(DepositMixin, SuccessMessageMixin, LoginRequiredMixin, generic.CreateView):
    model = Deposit
    form_class = DepositCreateForm
    initial = {'in_method': 'cash'}
    success_message = "Kaution von %(amount)s %(currency)s erfolgreich hinzugefügt."

    def form_valid(self, form):
        """
        Before validating the form, populate the person field using the request primary key as a lookup for
        """
        self.object = form.save(commit=False)
        self.object.person = Person.all_people.filter(pk=self.kwargs.get('pk')).get()
        self.object.in_datetime = timezone.now()
        self.object.save()
        logging.debug("Polulated the forms person field.")
        return super().form_valid(form)


class DepositRetain(DepositMixin, SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    model = Deposit
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
        logging.debug("Polulated the forms person field.")
        return super().form_valid(form)


class DepositReturn(DepositMixin, SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    model = Deposit
    form_class = DepositReturnForm
    template_name = 'keys/deposit_return_form.html'
    initial = {'out_method': 'cash'}
    success_message = "Kaution erfolgreich zurückgegeben."


    def form_valid(self, form):
        """
        Before validating the form, set active to False, the amount to 0 and note the out datetime
        """
        logging.debug('validating')
        self.object = form.save(commit=False)
        self.object.state = 'out'
        self.object.out_datetime = timezone.now()
        self.object.save()
        return super().form_valid(form)


class DepositDelete(DepositMixin, LoginRequiredMixin, generic.DeleteView):
    model = Deposit


# Rooms
class RoomList(LoginRequiredMixin, generic.ListView):
    model = Building
    template_name = "keys/room_list.html"


class RoomSearchResults(LoginRequiredMixin, generic.ListView):
    model = Room
    paginate_by = 30
    template_name_suffix = '_search_results'

    def get_queryset(self):
        # Alter the queryset of the list view, so that it only contains the entries
        # of the rooms match the search query in the get request
        query = self.request.GET.get('q')
        if query:
            room_list = Room.all_rooms.filter(models.Q(number__icontains=query) |
                                              models.Q(name__icontains=query) |
                                              models.Q(purpose__name__icontains=query) |
                                              models.Q(building__name__istartswith=query) |
                                              models.Q(building__identifier__istartswith=query) |
                                              models.Q(group__name__istartswith=query)
                                             )
        else:
            room_list = Room.all_rooms.all()

        return room_list



class RoomDetail(LoginRequiredMixin, generic.DetailView):
    model = Room


# Issues
class IssueList(LoginRequiredMixin, generic.ListView):
    model = Issue
    paginate_by = 20

    def get_queryset(self):
        # Alter the queryset of the list view, so that it only contains the issues
        # that have not yet been returend
        also_show_returned = self.request.GET.get('r')
        if not also_show_returned:
            issue_list = Issue.all_issues.active()
        else:
            issue_list = Issue.all_issues.all()

        return issue_list



class IssueSearchResults(LoginRequiredMixin, generic.ListView):
    model = Issue
    paginate_by = 20
    template_name_suffix = '_search_results'

    def get_queryset(self):
        # Alter the queryset of the list view, so that it only contains the entries
        # of the Issues where matching the search query in the get request
        query = self.request.GET.get('q','')
        show_returned = self.request.GET.get('r','')

        if show_returned:
            issue_list = Issue.all_issues.filter(models.Q(person__first_name__icontains=query) |
                                              models.Q(person__last_name__icontains=query) |
                                              models.Q(key__number__startswith=query)
                                             )
        else:
            issue_list = Issue.all_issues.active(models.Q(person__first_name__icontains=query) |
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
        person_id = self.request.GET.get('person','')
        if person_id:
            person = Person.all_people.get_person(person_id)
            context['person'] = person
            keys = Key.all_keys.availible()
            context['keys'] = keys
        return context

    def form_valid(self, form):
        """
        Before validating the form, set active to True and populate the person field using
        the request primary key as a lookup for
        """
        person_id = self.request.GET.get('person','')
        self.object = form.save(commit=False)
        self.object.person = Person.all_people.get_person(person_id)
        self.object.active = True
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('keys:person-detail',  args=[self.object.person.id])



class IssueReturnList(LoginRequiredMixin, generic.ListView):
    model = Issue
    paginate_by = 20



class IssueReturn(LoginRequiredMixin, generic.UpdateView):
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
        logging.debug("Before validating the form, set active to False")
        return super().form_valid(form)

