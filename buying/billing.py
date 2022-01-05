from .models import Invoice, Purchase
from collections import defaultdict


def get_billable_purchases(end_date):
    """
    Get all billable purchases until end_date
    for a certain depot.
    This includes all purchases that are not yet on an invoice.
    Returns a dictionary of users with their purchase items.
    """
    purchases = Purchase.objects.filter(
        date__lte=end_date,
        invoice__isnull=True
    )

    billables = defaultdict(list)
    for p in purchases:
        billables[p.user].append(p)

    return billables


def create_invoice(user, invoice_date, purchases):
    """
    create an invoice for a list of purchase items.
    """
    total_amount = sum([p.quantity * p.price for p in purchases])

    invoice = Invoice.objects.create(
        date=invoice_date,
        user=user,
        amount=total_amount
    )
    invoice.save()

    # add the items to invoice
    for item in purchases:
        item.invoice = invoice
        item.save()

    return invoice

def create_invoices(end_date, invoice_date):
    """
    Create invoices for all billable purchases
    until end_date
    """
    purch_per_user = get_billable_purchases(end_date)

    invoices = []
    for user, items in purch_per_user.items():
        invoice = create_invoice(user, invoice_date, items)
        invoices.append(invoice)

    return invoices



