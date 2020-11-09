from django.shortcuts import render, get_object_or_404
from django.views import View, generic
from django.http import HttpResponseRedirect, JsonResponse

from .models import Key, Person, Issue
from .forms import IssueReturnForm
# Create your views here:


def index_view(request):
    return render(request, 'keys/index.html')


# Keys
class KeyList(generic.ListView):
    model = Key
    paginate_by = 20


class KeyDetail(generic.DetailView):
    model = Key



# People
class PersonList(generic.ListView):
    model = Person
    paginate_by = 40


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

class IssueDetail(generic.DetailView):
    model = Issue

class IssueNew(generic.CreateView):
    model = Issue
    fields = ['person',
              'keys',
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
