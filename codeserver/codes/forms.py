from django import forms
from codes.models import Ticket

class RequestTicketsForm(forms.Form):
    # Get a CSV of tickets based on various filters
    pass

class UploadTicketsForm(forms.Form):
    # Upload a CSV of tickets that can optionally
    # all have a shared campaign, ex. date, max uses, etc
    pass
