from django import forms
from .models import Petition

class PetitionForm(forms.ModelForm):
    class Meta:
        model = Petition
        fields = ['movie_title', 'title', 'description']
        widgets = {
            'movie_title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Movie to add'}),
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Petition headline'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'rows':4, 'placeholder':'Why should we add it?'}),
        }