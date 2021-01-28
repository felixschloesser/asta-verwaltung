from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from keys.models import Person, Key
from .serializers import PersonSerializer, KeySerializer


class KeyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for listing or retrieving keys.
    """
    queryset = Key.all_keys
    serializer_class = KeySerializer
    permission_classes = [IsAuthenticated]


class PersonViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for listing or retrieving People.
    """
    queryset = Person.all_people
    serializer_class = PersonSerializer
    permission_classes = [IsAuthenticated]
