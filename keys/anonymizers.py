from gdpr import anonymizers

from .models import Person


class PersonContactDetailsAnonymizer(anonymizers.ModelAnonymizer):
    university_email = anonymizers.EmailFieldAnonymizer()
    private_email = anonymizers.EmailFieldAnonymizer()
    phone_number = anonymizers.CharFieldAnonymizer()

    class Meta:
        model = Person
        reversible_anonymization = False


# class PersonAnonymizer(anonymizers.DeleteModelAnonymizer):
    
#     class Meta:
#         model = Person
#         reversible_anonymization = False