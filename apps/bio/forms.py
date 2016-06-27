import datetime
from django.forms import ModelForm, widgets, ValidationError
from apps.bio.models import Person


class EditPersonForm(ModelForm):

    class Meta:
        model = Person

        widgets = {
            'bio': widgets.Textarea(),
            'other_contacts': widgets.Textarea()
        }

    def clean(self):
        cleaned_data = super(EditPersonForm, self).clean()
        date = cleaned_data.get("birthday")
        if date is None:
            raise ValidationError("Birthday date not correct!")
        elif date > datetime.date.today():
            raise ValidationError("The date cannot be in the future!")
        return cleaned_data
