from django import forms
from django_summernote.widgets import SummernoteWidget

from webapp.models import Property


class ObjectForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = '__all__'
        widgets = {
            'description': SummernoteWidget(),
            'notes': SummernoteWidget(),
            'many_rooms': SummernoteWidget(),
            'flour': SummernoteWidget(),
        }