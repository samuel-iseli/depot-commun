from .models import Invoice, Purchase
from collections import defaultdict


def get_billable_purchases(depot, end_date):
    """
    Get a list of billable purchases until end_date
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


def create_invoices(depot, end_date, invoice_date):
    """
    Create invoices for all billable purchases
    until end_date
    """
    invoices = []
    purchases = get_billable_purchases(depot, end_date)

    for purchase in purchases:
        invoice = Invoice.objects.create(
            date=invoice_date,
            depot=depot,
            # user=user
        )
        invoice.save()
        purchase.invoice=invoice
        purchase.save()

        invoices.append(invoice)

    return invoices



