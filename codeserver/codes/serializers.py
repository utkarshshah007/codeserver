from rest_framework import serializers
from codes.models import Bundle, Ticket, Scanner, Redemption

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('code', 'creation_datetime', 'bundle',
            'description', 'expiration_date', 'max_uses')

class ScannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scanner
        fields = ('name', 'location')

class RedemptionSerializer(serializers.ModelSerializer):
    ticket = serializers.StringRelatedField()
    scanner = ScannerSerializer()

    class Meta:
        model = Redemption
        fields = ('ticket', 'redemption_datetime',
            'redemption_location', 'scanner')
