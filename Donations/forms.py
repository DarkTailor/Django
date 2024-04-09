from django import forms

from .models import Donations



class DonationsForm(forms.ModelForm):
    class Meta:
        fields = ['type', 'amount', 'description']
        model = Donations


