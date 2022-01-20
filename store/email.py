from io import BytesIO
from smtplib import SMTPException
from django.core import mail
from .invoice_pdf import InvoicePdfRenderer
from django.core.validators import validate_email

def send_invoice_mails(invoices):
    """
    send out a list of invoices per e-mail.
    """
    success_count = 0
    failed_customers = []

    with mail.get_connection() as connection:
        for invoice in invoices:
            try:
                # check if customer has e-mail address
                validate_email(invoice.customer.email)

                message = create_invoice_message(connection, invoice)
                message.send(fail_silently=False)
                success_count += 1
            except Exception:
                failed_customers.append(invoice.customer)

    return (success_count, failed_customers)


def create_invoice_message(connection, invoice):
    """
    create an email message for an invoice.
    """
    # render pdf
    pdfstream = BytesIO()
    InvoicePdfRenderer().render(invoice, pdfstream)

    # create e-mail message
    message = mail.EmailMessage(
        subject='Depot Commün Rechnung',
        body=f'''Liebe/r {invoice.customer}

Beiliegend erhältst du deine Depot Commün Rechnung als PDF.
Bitte bezahle sie so bald wie möglich.

Liebe Grüsse
Dein Depot
''',
        to=[invoice.customer.email],
        connection=connection,
    )

    message.attach(
        f'Rechnung {invoice.id}',
        pdfstream.getvalue(),
        'application/pdf')

    return message
