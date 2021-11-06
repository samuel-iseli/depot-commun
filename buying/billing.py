from .models import Invoice, Purchase
from collections import defaultdict


def get_billable_purchases(depot, end_date):
    """
    Get a billable purchases until end_date
    for a certain depot.
    This includes all purchases that are not yet on an invoice.
    Returns a dictionary of users with their purchases.
    """
    purchases = Purchase.objects.filter(
        depot=depot,
        datetime__lte=end_date,
        invoice__isnull=True
    )

    billables = defaultdict(list)
    for purchase in purchases:
        billables[purchase.user].append(purchase)

    return billables


def create_invoice(depot, user, invoice_date, purchases):
    total_amount = sum([p.total_price for p in purchases])

    invoice = Invoice.objects.create(
        date=invoice_date,
        depot=depot,
        user=user,
        amount=total_amount
    )
    invoice.save()

    for purchase in purchases:
        purchase.invoice = invoice
        purchase.save()

    return invoice


def create_invoices(depot, end_date, invoice_date):
    """
    Create invoices for all billable purchases
    until end_date
    """
    purchases_per_user = get_billable_purchases(depot, end_date)

    invoices = []
    for user, purchases in purchases_per_user.items():
        invoice = create_invoice(depot, user, invoice_date, purchases)
        invoices.append(invoice)

    return invoices



