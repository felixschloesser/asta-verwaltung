# api/serializers.py
from rest_framework import serializers
from keys.models import Person


class PersonSerializer(serializers.ModelSerializer):
        class Meta:
            model = Person
            fields = ('first_name', 'last_name', 'university_email')

