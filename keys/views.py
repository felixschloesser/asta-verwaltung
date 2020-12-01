from django.shortcuts import render, get_object_or_404
from django.views import View, generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.urls import reverse_lazy
from django.http import Http404

from .models import Key, Person, Issue, Deposit
from .forms import IssueReturnForm, DepositCreateForm
# Create your views here:


def index_view(request):
    return render(request, 'keys/index.html')


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
        key_list = Key.objects.filter(models.Q(number__startswith=query) |
                                      models.Q(locking_system__name__icontains=query) |
                                      models.Q(locking_system__company__icontains=query)
                                     )
        return key_list

class KeyDetail(LoginRequiredMixin, generic.DetailView):
    model = Key



# People
class PersonList(LoginRequiredMixin, generic.ListView):
    model = Person
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
        person_list = Person.objects.filter(models.Q(first_name__startswith=query) |
                                            models.Q(last_name__startswith=query)
                                           )
        return person_list


class PersonCreate(LoginRequiredMixin, generic.CreateView):
    model = Person
    fields = ['first_name',
              'last_name',
              'university_email',
              'private_email',
              'phone_number',
              'group']


class PersonDetail(LoginRequiredMixin, generic.DetailView):
    model = Person


class PersonUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Person
    fields = ['first_name',
              'last_name',
              'university_email',
              'private_email',
              'phone_number',
              'group']
    template_name_suffix = '_update_form'


class PersonCreateDeposit(LoginRequiredMixin, generic.CreateView):
    model = Deposit
    form_class = DepositCreateForm
    template_name = 'keys/person_create_deposit_form.html'

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
        person = Person.objects.filter(pk=self.kwargs.get('pk')).get()
        context["person"] = person
        return context

    def form_valid(self, form):
        """
        Before validating the form, populate the person field using the request primary key as a lookup for
        """
        self.object = form.save(commit=False)
        self.object.person = Person.objects.filter(pk=self.kwargs.get('pk')).get()
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('keys:person-detail', args = [self.object.person.id])


class PersonUpdateDeposit(LoginRequiredMixin, generic.UpdateView):
    model = Deposit
    fields = ['amount',
              'currency',
              'in_datetime',
              'in_method']

    template_name = 'keys/person_update_deposit_form.html'

    def get_success_url(self):
        return reverse_lazy('keys:person-detail', args = [self.object.person.id])

    def get_object(self, queryset=None):
        """
        Get the deposit from the person-pk in the urlpattern.
        """
        queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        obj = queryset.filter(person__id=pk).get()
        return obj


class PersonReturnDeposit(LoginRequiredMixin, generic.UpdateView):
    model = Deposit
    fields = ['out_datetime',
              'out_method']

    template_name = 'keys/person_return_deposit_form.html'

    def get_success_url(self):
        return reverse_lazy('keys:person-detail', args = [self.object.person.id])

    def get_object(self, queryset=None):
        """
        Get the deposit from the person-pk in the urlpattern.
        """
        queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        obj = queryset.filter(person__id=pk).get()
        return obj

# Issues
class IssueList(LoginRequiredMixin, generic.ListView):
    model = Issue
    paginate_by = 20

    def get_queryset(self):
        # Alter the queryset of the list view, so that it only contains the issues
        # that have not yet been returend
        show_returned = self.request.GET.get('r')
        if show_returned:
            issue_list = Issue.objects.filter()
        else:
            issue_list = Issue.objects.filter(in_date__isnull=True)

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
            issue_list = Issue.objects.filter(models.Q(person__first_name__icontains=query) |
                                              models.Q(person__last_name__icontains=query) |
                                              models.Q(key__number__startswith=query)
                                             )
        else:
            issue_list = Issue.objects.filter(models.Q(person__first_name__icontains=query) |
                                            models.Q(person__last_name__icontains=query) |
                                            models.Q(key__number__startswith=query),
                                            in_date__isnull=True
                                           )
        return issue_list


class IssueDetail(LoginRequiredMixin, generic.DetailView):
    model = Issue


class IssueNew(LoginRequiredMixin, generic.CreateView):
    model = Issue
    fields = ['person',
              'key',
              'out_date']


class IssueReturnList(LoginRequiredMixin, generic.ListView):
    model = Issue
    paginate_by = 20


class IssueReturn(LoginRequiredMixin, generic.UpdateView):
    model = Issue
    form_class = IssueReturnForm
    template_name_suffix ='_return_form'
