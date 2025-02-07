from .models import Invoice


def create_invoice(customer, invoice_date, purchases):
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

    return invoice
