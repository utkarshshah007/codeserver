from django import forms
from codes.models import Ticket, Bundle

class RequestTicketsForm(forms.Form):
    # Get a CSV of tickets based on various filters
    pass

class CreateTicketsForm(forms.Form):
    ticket_numbers = forms.CharField(help_text='Enter one or more ticket numbers seperated by commas')
    bundle = forms.ModelChoiceField(queryset=Bundle.objects.all(), required=False)
    description = forms.CharField(required=False)
    expiration_date = forms.DateTimeField(required=False, widget=forms.SelectDateWidget)
    max_uses = forms.IntegerField(required=False)
