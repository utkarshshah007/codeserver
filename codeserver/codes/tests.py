import string
import random
import datetime

from django.test import TestCase
from django.utils import timezone
from .models import Bundle, Ticket, Scanner, Redemption

def datetimeWithOffset(days):
	return timezone.now() + datetime.timedelta(days=days)

def sample_code(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

# Create your tests here.
class TicketModelTests(TestCase):
	def test_create_one_code(self):
		code = sample_code()
		ticket = Ticket.objects.create(code=code)

		self.assertIsInstance(ticket, Ticket)
		self.assertEqual(ticket.code, code)

	def test_create_multiple_codes(self):
		n = random.randint(5,10)
		codes = [sample_code() for _ in range(n)]
		tickets = [Ticket.objects.create(code=code) for code in codes]
		self.assertEqual(len(tickets), n)
		self.assertTrue(all([tickets[i].code == codes[i] for i in range(n)]))

	def test_generate_one_code(self):
		[ticket] = Ticket.objects.generate()

		self.assertIsInstance(ticket, Ticket)
		self.assertIsNotNone(ticket.code)

	def test_generate_multiple_codes(self):
		n = random.randint(5,10)
		tickets = Ticket.objects.generate(num=n)
		self.assertEqual(len(tickets), n)
		
		for ticket in tickets:
			self.assertIsInstance(ticket, Ticket)
			self.assertIsNotNone(ticket.code)

	def test_duplicate_codes(self):
		t = Ticket.objects.create(code="ABC")

		with self.assertRaises(Exception):
			Ticket.objects.create(code="ABC")

	def test_unlimited_use_code(self):
		code = sample_code()
		ticket = Ticket.objects.create(code=code)
		ticket.creation_datetime = datetimeWithOffset(days=-365)

		for _ in range(random.randint(1,20)):
			self.assertTrue(ticket.validate())
			self.assertIsInstance(ticket.redeem(), Redemption)

	def test_single_use_code(self):
		code = sample_code()
		ticket = Ticket.objects.create(code=code, max_uses=1)
		self.assertTrue(ticket.validate())
		self.assertIsInstance(ticket.redeem(), Redemption)

		self.assertFalse(ticket.validate())
		with self.assertRaises(ValueError):
			ticket.redeem()

	def test_multiple_use_code(self):
		n = random.randint(5,10)
		code = sample_code()
		ticket = Ticket.objects.create(code=code, max_uses=n)

		for i in range(n):
			self.assertTrue(ticket.validate())
			self.assertIsInstance(ticket.redeem(), Redemption)

		self.assertFalse(ticket.validate())
		with self.assertRaises(ValueError):
			ticket.redeem()

	def test_code_with_expiration(self):
		code = sample_code()
		ticket = Ticket.objects.create(code=code, expiration_date=datetimeWithOffset(1))
		self.assertTrue(ticket.validate())
		self.assertIsInstance(ticket.redeem(), Redemption)

		code = sample_code()
		ticket = Ticket.objects.create(code=code, expiration_date=datetimeWithOffset(-1))
		self.assertFalse(ticket.validate())
		with self.assertRaises(ValueError):
			ticket.redeem()

	def test_code_with_no_expiration(self):
		code = sample_code()
		ticket = Ticket.objects.create(code=code)
		ticket.creation_datetime = datetimeWithOffset(days=-365)

		self.assertTrue(ticket.validate())
		self.assertIsInstance(ticket.redeem(), Redemption)

	def test_code_with_expiration_and_limited_use(self):
		code = sample_code()
		ticket = Ticket.objects.create(code=code, max_uses=1, expiration_date=datetimeWithOffset(1))
		self.assertTrue(ticket.validate())
		self.assertIsInstance(ticket.redeem(), Redemption)

		self.assertFalse(ticket.validate())
		with self.assertRaises(ValueError):
			ticket.redeem()

		code = sample_code()
		ticket = Ticket.objects.create(code=code, max_uses=1, expiration_date=datetimeWithOffset(-1))
		self.assertFalse(ticket.validate())
		with self.assertRaises(ValueError):
			ticket.redeem()


class BundleModelTests(TestCase):
	def test_create_empty_bundle(self):
		bundle = Bundle.objects.create(name="Test Bundle")
		self.assertIsInstance(bundle, Bundle)
		self.assertEqual(bundle.ticket_set.count(), 0)

	def test_create_bundle_with_codes(self):
		bundle = Bundle.objects.create(name="Test Bundle")

		n = random.randint(5,10)
		codes = [sample_code() for _ in range(n)]
		for code in codes:
			bundle.ticket_set.create(code=code)

		self.assertEqual(bundle.ticket_set.count(), n)
		tickets = list(bundle.ticket_set.all())
		self.assertTrue(all([tickets[i].code == codes[i] for i in range(n)]))

	def test_create_bundle_generate_codes(self):
		bundle = Bundle.objects.create(name="Test Bundle")

		n = random.randint(5,10)
		bundle.ticket_set.generate(num=n)

		self.assertEqual(bundle.ticket_set.count(), n)
		for ticket in bundle.ticket_set.all():
			self.assertIsInstance(ticket, Ticket)
			self.assertIsNotNone(ticket.code)

	def test_add_ticket_to_bundle(self):
		bundle = Bundle.objects.create(name="Test Bundle")
		ticket1 = Ticket.objects.create(code=sample_code())
		ticket2  = Ticket.objects.create(code=sample_code())

		bundle.ticket_set.add_to_bundle(ticket1, ticket2)

		self.assertEqual(bundle.ticket_set.count(), 2)
		self.assertTrue(bundle.ticket_set.filter(pk=ticket1.pk).exists())
		self.assertTrue(bundle.ticket_set.filter(pk=ticket2.pk).exists())

	def test_tickets_inherit_from_bundle_create(self):
		desc = "A simple test case"
		date = datetimeWithOffset(2)
		uses = 4
		bundle = Bundle.objects.create(name="Test Bundle", description=desc, 
			expiration_date=date, max_uses_per_ticket=uses)

		bundle.ticket_set.create(code=sample_code())
		ticket = bundle.ticket_set.last()

		self.assertEqual(ticket.description, desc)
		self.assertEqual(ticket.expiration_date, date)
		self.assertEqual(ticket.max_uses, uses)

	def test_tickets_inherit_from_bundle_add(self):
		desc = "A simple test case"
		date = datetimeWithOffset(2)
		uses = 4
		bundle = Bundle.objects.create(name="Test Bundle", description=desc, 
			expiration_date=date, max_uses_per_ticket=uses)
		ticket = Ticket.objects.create(code=sample_code())

		bundle.ticket_set.add_to_bundle(ticket)
		ticket = bundle.ticket_set.last()

		self.assertEqual(ticket.description, desc)
		self.assertEqual(ticket.expiration_date, date)
		self.assertEqual(ticket.max_uses, uses)


class ScannerModelTests(TestCase):
	def setUp(self):
		# Create scanner
		pass

	def test_scan_code_pass(self):
		pass

	def test_scan_code_fail(self):
		pass

class RedemptionModelTests(TestCase):
	def setUp(self):
		# Create tickets
		# Create bundle
		# Create scanner
		pass

	def test_redeem_no_scanner_info(self):
		pass

	def test_redeem_scanner_info(self):
		pass

	def test_redeem_scanner_changed(self):
		pass

