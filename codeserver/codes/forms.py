from django import forms
from codes.models import Ticket

class RequestTicketsForm(forms.Form):
    # Get a CSV of tickets based on various filters
    pass

class UploadTicketsForm(forms.Form):
    # Upload a CSV of tickets that can optionally
    # all have a shared campaign, ex. date, max uses, etc
    pass

class ScanTicketForm(forms.Form):
    # Accept a Ticket number, then validate and/or redeem it
    ticket_number = forms.CharField()
