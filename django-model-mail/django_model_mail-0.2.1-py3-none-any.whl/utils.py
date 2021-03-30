from django.utils.hashable import make_hashable
from django.utils.encoding import force_str


def get_choice_display(field, value):
    choices_dict = dict(make_hashable(field.flatchoices))
    # force_str() to coerce lazy strings.
    return force_str(choices_dict.get(make_hashable(value), value), strings_only=True)
