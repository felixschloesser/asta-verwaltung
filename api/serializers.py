# api/serializers.py
from rest_framework import serializers
from keys.models import Person, Key, Room


class PersonSerializer(serializers.ModelSerializer):
        class Meta:
            model = Person
            fields = ('first_name', 'last_name', 'university_email')

class KeySerializer(serializers.ModelSerializer):
        class Meta:
            model = Key
            fields = ('number', 'locking_system')


class RoomSerializer(serializers.ModelSerializer):
        class Meta:
            model = Room
            fields = ('building', 'number')
