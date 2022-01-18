from io import BytesIO
from smtplib import SMTPException
from django.core import mail
from .invoice_pdf import InvoicePdfRenderer


def send_invoice_mails(invoices):
    """
    send out a list of invoices per e-mail.
    """
    success_count = 0
    failed_addresses = []

    with mail.get_connection() as connection:
        for invoice in invoices:
            message = create_invoice_message(connection, invoice)
            try:
                message.send(fail_silently=False)
                success_count += 1
            except SMTPException:
                failed_addresses.append(invoice.customer.email)

    return (success_count, failed_addresses)


def create_invoice_message(connection, invoice):
    """
    create an email message for an invoice.
    """

    # render pdf
    pdfstream = BytesIO()
    InvoicePdfRenderer().render(invoice, pdfstream)

    # create e-mail message
    message = mail.EmailMessage(
        'Depot Commün Rechnung',
        f'''Liebe/r {invoice.customer}

Beiliegend erhältst du deine Depot Commün Rechnung als PDF.
Bitte bezahle sie so bald wie möglich.

Liebe Grüsse
Dein Depot
''',
    'mail@depotcommun.ch',
    [invoice.customer.email],
    connection=connection,
    )

    message.attach(
        f'Rechnung {invoice.id}',
        pdfstream.getvalue(),
        'application/pdf')

    return message
