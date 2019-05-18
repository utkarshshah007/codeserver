from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
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


class ScanTicketView(TemplateView):
    """
    An Example Implementation of an API Client Scanner.
    Uses the ScanTicketAPIView to scan.
    """
    template_name = 'codes/scan_ticket.html'
