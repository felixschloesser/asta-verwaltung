from django.shortcuts import render, get_object_or_404
from django.views import View, generic
from django.http import HttpResponseRedirect, JsonResponse
from django.db import models

from .models import Key, Person, Issue
from .forms import IssueReturnForm
# Create your views here:


def index_view(request):
    return render(request, 'keys/index.html')


# Keys
class KeyList(generic.ListView):
    model = Key
    paginate_by = 20


class KeySearchResults(generic.ListView):
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

class KeyDetail(generic.DetailView):
    model = Key



# People
class PersonList(generic.ListView):
    model = Person
    paginate_by = 30


class PersonSearchResults(generic.ListView):
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


class PersonDetail(generic.DetailView):
    model = Person


class PersonCreate(generic.CreateView):
    model = Person
    fields = ['first_name',
              'last_name',
              'university_email',
              'private_email',
              'phone_number',
              'group']


# Issues
class IssueList(generic.ListView):
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


class IssueSearchResults(generic.ListView):
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


class IssueDetail(generic.DetailView):
    model = Issue


class IssueNew(generic.CreateView):
    model = Issue
    fields = ['person',
              'key',
              'out_date']

class IssueReturnList(generic.ListView):
    model = Issue
    paginate_by = 20


class IssueReturn(generic.UpdateView):
    model = Issue
    form_class = IssueReturnForm
    template_name_suffix ='_return_form'



# class IssueCreate(View):
#     form_class = IssueForm
#     initial = {'key': 'value'}
#     template_name = 'keys/issue_form.html'

#     def get(self, request):
#         self.form = self.form_class(request.POST)

#         # Name autocompletion /?name='Felix'
#         if 'term' in request.GET:
#             qs = Person.objects.filter(first_name__istartswith=request.GET.get('term'))
#             autocomplete_names = [person.first_name + ' ' +
#                                   person.last_name for person in qs]
#             return JsonResponse(autocomplete_names, safe=False)
#             # safe=false allows also lists not only dicts to be serialized

#         # Regular GET
#         else:
#             return render(request, self.template_name, {'form': self.form})

#     def post(self, request):
#         self.form = self.form_class(request.POST)
#         if self.form.is_valid():
#             self.form.save()
#             return HttpResponseRedirect('/keys/issues')

#         return render(request, self.template_name, {'form': self.form})


# Schlüssel zurückgeben:
    #termin vereinbaren

# Meine Schlüssel
