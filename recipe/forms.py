from django import forms
from tinymce.widgets import TinyMCE
from .models import Direction, Recipe

class DirectionForm(forms.ModelForm):
    rich_text = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows':50,'class': 'form-control'}))
    class Meta:
        model = Direction
        exclude = ()
