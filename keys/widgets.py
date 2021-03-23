from django.forms.widgets import Select


class Datalist(Select):
    input_type = 'text'
    template_name = 'widgets/datalist.html'
    option_template_name = 'widgets/datalist_option.html'
    add_id_index = False
    checked_attribute = {'selected': True}
    option_inherits_attrs = False