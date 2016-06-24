from django.forms import ModelForm, widgets
from apps.bio.models import Person


class EditPersonForm(ModelForm):

    class Meta:
        model = Person

        widgets = {
            'bio': widgets.Textarea(),
            'other_contacts': widgets.Textarea()
        }
