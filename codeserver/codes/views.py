from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import FormView
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer

from urllib.parse import urlencode

from codes.forms import ScanTicketForm
from codes.models import Ticket, Scanner, Redemption
from codes.serializers import TicketSerializer, RedemptionSerializer


def index(request):
    return redirect('scan-ticket')


class ScanTicketAPIView(APIView):
    renderer_classes = (JSONRenderer, )

    def post(self, request):
        """
        Requires: ticket_number, scanner_id

        If the ticket exists, scan it with the provided scanner.
        Return the result of the scan & the ticket's full redemption history.

        If the ticket does not exist, returns 404
        """
        missing = ("ticket_number" not in request.data
                        or "scanner_id" not in request.data)
        if missing:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        ticket_number = request.data['ticket_number']
        scanner_id = request.data['scanner_id']

        try:
            ticket = Ticket.objects.get(code=ticket_number)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Scan the ticket with the provided scanner_id
        scanner = Scanner.objects.get(pk=scanner_id)
        redemption = scanner.scan(ticket)

        history = ticket.redemption_set.all()

        data = {
            "valid": True if redemption else False,
            "ticket": TicketSerializer(ticket).data,
            "redemption_list": RedemptionSerializer(history, many=True).data
        }

        return Response(data, status=status.HTTP_200_OK)


class ScanTicketView(FormView):
    template_name = 'codes/scan_ticket.html'
    form_class = ScanTicketForm

    def form_valid(self, form):
        # This method is called when someone scans a ticket
        # It redeems that ticket & displays the ticket's redemption history

        # Get the ticket, if it exists
        code = form.cleaned_data["ticket_number"]
        try:
            ticket = Ticket.objects.get(code=code)
        except Exception as e:
            print("could not find ticket with code: ", code)
            return redirect('scan-ticket')

        # Scan the ticket with the Web Scanner
        scanner = Scanner.objects.get(pk=2)
        redemption = scanner.scan(ticket)

        # Create a result query string to redirect to
        base_url = reverse('scan-ticket')
        ticket_query_string =  urlencode({'ticket': ticket.id})
        url = '{}?{}'.format(base_url, ticket_query_string)
        if redemption:
            redemption_query_string = urlencode({'redemption': redemption.id})
            url = '{}&{}'.format(url, redemption_query_string)
        return redirect(url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'code' in self.request.GET:
            context['code'] = self.request.GET.get('code')
        if 'ticket' in self.request.GET:
            context['ticket'] = Ticket.objects.get(pk=self.request.GET.get('ticket'))
        if 'redemption' in self.request.GET:
            context['redemption'] = Redemption.objects.get(pk=self.request.GET.get('redemption'))
        return context
