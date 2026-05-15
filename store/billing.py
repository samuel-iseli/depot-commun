from .models import Invoice, Purchase, ShoppingBasket
from collections import defaultdict


def get_billable_baskets(end_date):
    """
    Get all completed shopping baskets until end_date that are not yet on an invoice.
    Returns a dictionary of customers with their completed baskets.
    """
    baskets = ShoppingBasket.objects.filter(
        completed__isnull=False,
        completed__lte=end_date,
        invoice__isnull=True,
        customer__isnull=False,
    )

    billables = defaultdict(list)
    for basket in baskets:
        billables[basket.customer].append(basket)

    return billables


def create_invoice(customer, invoice_date, purchases, baskets=None):
    """
    create an invoice for a list of purchase items.
    """
    total_amount = sum([p.quantity * p.price for p in purchases])

    invoice = Invoice.objects.create(
        date=invoice_date,
        customer=customer,
        amount=total_amount
    )
    invoice.save()

    # add the items to invoice
    for item in purchases:
        item.invoice = invoice
        item.save()

    for item in baskets or []:
        item.invoice = invoice
        item.save()

    return invoice

def create_basket_invoices(end_date, invoice_date):
    """
    Create invoices for all completed shopping baskets that are not yet invoiced.
    Baskets are grouped by customer and attached to one invoice per customer.
    """
    baskets_per_user = get_billable_baskets(end_date)

    invoices = []
    for customer, baskets in baskets_per_user.items():
        invoice = create_invoice(customer, invoice_date, [], baskets=baskets)
        invoices.append(invoice)

    return invoices



