from django import forms
from .models import *
from django.forms import widgets
class FileForm(forms.ModelForm):
    class Meta:
        model=Upload
        fields=['file',"public"]

class CsvForm(forms.ModelForm):
    class Meta:
        model=Csv
        fields=['file','date']
        widgets = {
            'date': widgets.DateInput(attrs={'type': 'date'})
        }