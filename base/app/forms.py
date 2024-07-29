from django import forms
from .views import DownloadForm

class DownloadForm(forms.Form):
    url = forms.CharField(widget=forms.TextInput(attrs={ 'placeholder': 'Enter video url' }), label=False)
