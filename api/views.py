# api/views.py
from rest_framework import generics


from keys.models import Person
from .serializers import PersonSerializer

class PersonAPIView(generics.ListAPIView):
    queryset = Person.all_people.all()
    serializer_class = PersonSerializer
