from django.forms.widgets import Select
from django.forms import TextInput, MultiWidget


class Datalist(Select):
    input_type = 'text'
    template_name = 'widgets/datalist.html'
    option_template_name = 'widgets/datalist_option.html'
    add_id_index = False
    checked_attribute = {'selected': True}
    option_inherits_attrs = False



class FullNameWidget(MultiWidget):
    def __init__(self, attrs={}):
        _widgets = (
            TextInput(attrs=attrs),
            TextInput(attrs=attrs)
        )

        super(ExpiryDateWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        return [value.month, value.year] if value else [None, None]
