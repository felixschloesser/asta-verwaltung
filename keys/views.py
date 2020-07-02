from django.shortcuts import render
from django.views import generic

from .models import Key

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'keys/index.html'
    context_object_name = 'latest_key_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Key.objects.all()

# Schlüssel ausleiehn
    # If logged in: termin vereinbaren
    #

# Schlüssel zurückgeben:
    #termin vereinbaren

# Meine Schlüssel
