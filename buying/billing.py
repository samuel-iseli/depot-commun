from .models import Invoice, Purchase
from collections import defaultdict


def get_billable_purchases(depot, end_date):
    """
    Get all billable purchases until end_date
    for a certain depot.
    This includes all purchases that are not yet on an invoice.
    Returns a dictionary of users with their purchase items.
    """
    purchases = Purchase.objects.filter(
        depot=depot,
        datetime__lte=end_date,
        invoice__isnull=True
    )

    billables = defaultdict(list)
    for p in purchases:
        billables[p.user].append(p)

    return billables


def create_invoice_from_purchases(depot, user, invoice_date, purchases):
    # get all the items from the purchases
    p_items = [itm for p in purchases for itm in p.items.all()]

    invoice = create_invoice(depot, user, invoice_date, p_items)

    # additinally add the purchase objects to invoice
    for purch in purchases:
        purch.invoice = invoice
        purch.save()

    return invoice

def create_invoice(depot, user, invoice_date, itempurchases):
    """
    create an invoice for a list of purchase items.
    """
    total_amount = sum([p.quantity * p.price for p in itempurchases])

    invoice = Invoice.objects.create(
        date=invoice_date,
        depot=depot,
        user=user,
        amount=total_amount
    )
    invoice.save()

    # add the items to invoice
    for item in itempurchases:
        item.invoice = invoice
        item.save()

    return invoice

def create_invoices(depot, end_date, invoice_date):
    """
    Create invoices for all billable purchases
    until end_date
    """
    p_items_per_user = get_billable_purchases(depot, end_date)

    invoices = []
    for user, items in p_items_per_user.items():
        invoice = create_invoice_from_purchases(depot, user, invoice_date, items)
        invoices.append(invoice)

    return invoices



