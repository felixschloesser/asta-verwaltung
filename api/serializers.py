# api/serializers.py
from rest_framework import serializers
from keys.models import Person, Key, Room

from hashid_field.rest import HashidSerializerCharField


class PersonSerializer(serializers.HyperlinkedModelSerializer):
    id = HashidSerializerCharField(source_field='keys.Person.id', read_only=True)

    class Meta:
        model = Person
        fields = ('url', 'id', 'first_name', 'last_name', 'university_email')



class KeySerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Key
        fields = ('url', 'id', 'number', 'locking_system')
        extra_kwargs = {
            'locking_system': {'lookup_field': 'id'}
        }


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Room
        fields = ('url', 'id', 'building', 'number')



class LockingSystemSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Room
        fields = ('id', 'name', 'company')
