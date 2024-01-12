from django import forms
from django.core.exceptions import ValidationError
from .models import *


class AddImageForm(forms.ModelForm):

    class Meta:
        model = Images
        fields = ['photo', 'description', 'slug']

    def clean_description(self):
        description = self.cleaned_data['description']
        if len(description) > 200:
            raise ValidationError('len more then 200 symbols')
        return description


class PhotoFilterForm(forms.Form):
    search = forms.CharField(required=False)
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
