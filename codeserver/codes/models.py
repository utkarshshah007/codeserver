import uuid

from django.db import models
from django.utils import timezone

class Bundle(models.Model):
    name = models.CharField(max_length=80)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=160, blank=True)
    expiration_date = models.DateTimeField(null=True, blank=True)
    max_uses_per_ticket = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class TicketManager(models.Manager):

    # Override for create to allow autofill based on bundle info
    def create(self, **kwargs):
        ticket = super().create(**kwargs)

        if ticket.bundle:
            if "description" not in kwargs: ticket.description = ticket.bundle.description
            if "expiration_date" not in kwargs: ticket.expiration_date = ticket.bundle.expiration_date
            if "max_uses" not in kwargs: ticket.max_uses = ticket.bundle.max_uses_per_ticket
            ticket.save()
        
        return ticket

    # Override for add to allow update based on bundle info
    def add_to_bundle(self, *objs, **kwargs):
        bundle = self.instance

        if bundle is None:
            raise AttributeError("No Bundle instance found")

        for ticket in objs:
            ticket.description = bundle.description
            ticket.expiration_date = bundle.expiration_date
            ticket.max_uses = bundle.max_uses_per_ticket
            ticket.save()

        self.add(*objs, **kwargs)

    # Create new ticket from auto-generated ID - returns Ticket or list of Tickets
    def generate(self, num=1):
        codes = []
        for n in range(num):
            code = uuid.uuid4().hex.upper()
            codes.append(self.create(code=code))
        return codes


class Ticket(models.Model):
    code = models.CharField(max_length=36, unique=True)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    bundle = models.ForeignKey(Bundle, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=160, blank=True)
    expiration_date = models.DateTimeField(null=True, blank=True)
    max_uses = models.IntegerField(null=True, blank=True)

    objects = TicketManager()

    # Check if ticket is valid - return boolean
    def validate(self):
        if self.expiration_date is not None:
            if self.expiration_date < timezone.now():
                return False

        if self.max_uses is not None:
            used = self.redemption_set.count()
            if self.max_uses <= used:
                return False

        return True


    # Use the ticket, if it is valid - return Redemption
    def redeem(self):
        if not self.validate():
            raise ValueError("Cannot redeem invalid Ticket");

        return self.redemption_set.create()

    def __str__(self):
        return self.code


class Scanner(models.Model):
    name = models.CharField(max_length=80)
    location = models.CharField(max_length=200, blank=True)

    # Validate & Redeem the ticket, add Scanner info - return Redemption
    def scan(self, ticket):
        if not ticket.validate():
            return None

        redemption = ticket.redeem()
        redemption.scanner = self
        redemption.redemption_location = self.location
        redemption.save()

        return redemption

    def __str__(self):
        return self.name


class Redemption(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    redemption_datetime = models.DateTimeField(auto_now_add=True)
    redemption_location = models.CharField(max_length=200, blank=True)
    scanner = models.ForeignKey(Scanner, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.ticket.code + " @ " + self.redemption_datetime.strftime('%Y-%m-%d %I:%M %p')