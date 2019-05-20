from django.shortcuts import redirect
from django.views import generic
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

from codes.models import Ticket, Scanner, Redemption
from codes.forms import CreateTicketsForm
from codes.serializers import TicketSerializer, RedemptionSerializer


class IndexView(generic.TemplateView):
    template_name = 'codes/dashboard.html'

class DocView(generic.View):
    def get(self, request):
        return redirect("https://documenter.getpostman.com/view/144103/S1M3wm34")


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


class ScanTicketView(generic.TemplateView):
    """
    An Example Implementation of an API Client Scanner.
    Uses the ScanTicketAPIView to scan.
    """
    template_name = 'codes/scan_ticket.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['scanners'] = Scanner.objects.all()
        return context


@method_decorator(staff_member_required, name='dispatch')
class CreateTicketsView(generic.edit.FormView):
    template_name = 'codes/create_tickets.html'
    form_class = CreateTicketsForm
    success_url = '/admin/codes/ticket/'

    """
    Requires:
    - a list of ticket_numbers
    # TODO:
    OR
    - generate = True
    - num_to_generate >= 1

    Optional:
    - bundle
    - description
    - expiration_date
    - max_uses

    Registers (TODO: or generates) new tickets with the info specified.
    """

    def form_valid(self, form):
        # Split into individual ticket numbers
        str = form.cleaned_data["ticket_numbers"]
        ticket_numbers = [s.strip() for s in str.split(',')]

        # Get any additional info
        keys = ["bundle","description","expiration_date","max_uses"]
        kwargs = {k: v for k, v in form.cleaned_data.items() if (
                        k in keys and v is not None)}

        # TODO: Generate tickets if required

        # Create tickets
        for ticket_number in ticket_numbers:
            Ticket.objects.create(code=ticket_number, **kwargs)

        # Return
        return super().form_valid(form)
