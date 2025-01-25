from django import forms
from django import forms

class ArxivSearchForm(forms.Form):
     mot_cle = forms.CharField(label="Mot-clé", required=False)
     date_debut = forms.DateField(
        label="Date de début",
        required=False,
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "date-field"  # optional extra class
            }
        )
    )
     date_fin = forms.DateField(
        label="Date de fin",
        required=False,
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "date-field"  # optional extra class
            }
        )
    )



class ScholarSearchForm(forms.Form):
    mot_cle = forms.CharField(label='Mot-clé', max_length=100)
    date_debut = forms.DateField(label="Date de début", widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    date_fin = forms.DateField(label="Date de fin", widget=forms.DateInput(attrs={'type': 'date'}), required=True)

class ScholarsemSearchForm(forms.Form):
    mot_cle = forms.CharField(max_length=100)


# veille_app/forms.py
from django import forms

from django import forms

class PLOSOneSearchForm(forms.Form):
    mot_cle = forms.CharField(label="Mot-clé", required=False)
    date_debut = forms.DateField(
        label="Date de début",
        required=False,
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "date-field"  # optional extra class
            }
        )
    )
    date_fin = forms.DateField(
        label="Date de fin",
        required=False,
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "date-field"  # optional extra class
            }
        )
    )

from .models import Rapport
class RapportForm(forms.ModelForm):
    class Meta:
        model = Rapport
        fields = ['titre']

from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['remarks', 'analysis']