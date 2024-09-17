# forms.py

from django import forms

class MoleculeSearchForm(forms.Form):
    mol_id = forms.CharField(max_length=100, required=True, label='')
