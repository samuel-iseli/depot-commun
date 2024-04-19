import time
from io import BytesIO
from django.utils import timezone
from threading import Thread
from django.core import mail
from .invoice_pdf import InvoicePdfRenderer
from .models import EmailTask
from django.core.validators import validate_email

# batch size for sending e-mails per connection to the mail server
BATCH_SIZE = 10


def send_invoice_mails(invoices):
    """
    send out a list of invoices per e-mail.
    """
    mailer = InvoiceMailer(invoices)
    mailer.send()

    return mailer.success, mailer.progress_message


class InvoiceMailer:
    def __init__(self, invoices):
        self.invoices = invoices
        self.log_lines = []
        self.success = False
        self.success_count = 0

    def send(self):
        if len(self.invoices) <= BATCH_SIZE:
            # send e-mail directly without starting a thread
            self.internal_send_invoice_mails()
            if self.success:
                self.progress_message = "%d Rechnungen verschickt" % self.success_count
            else:
                self.progress_message = "%d Rechnungen verschickt, %d Fehler" % (self.success_count, len(self.invoices)-self.success_count)
            return

        # start a thread to send e-mails
        # set success for immediate feedback, may be changed later
        self.success = True
        t = Thread(target=self.internal_send_invoice_mails)
        t.start()
        self.progress_message = "%d Rechnungen werden im Hintergrund verschickt" % len(self.invoices)

    def internal_send_invoice_mails(self):
        start_time = timezone.now()
        success = True

        start = 0
        batch = self.invoices[start:start+BATCH_SIZE]
        start = start+BATCH_SIZE

        while batch:
            try:
                with mail.get_connection() as connection:
                    for invoice in batch:
                        try:
                            # check if customer has e-mail address
                            validate_email(invoice.customer.email)
                            message = self.create_invoice_message(connection, invoice)
                            try:
                                message.send(fail_silently=False)
                                self.add_log("OK Invoice %d to %s" % (invoice.id, message.to[0]))
                                self.success_count += 1
                                invoice.email_sent = True
                            except Exception as e:
                                success = False
                                self.add_log("Error on sending message to %s: %s" % (message.to[0], str(e)))

                        except Exception as e:
                            success = False
                            self.add_log("Error on creating message for invoice %d: %s" % (invoice.id, str(e)))
            except Exception as e:
                success = False
                self.add_log("Error on connecting to smtp server: %s" % str(e))

            batch = self.invoices[start:start+BATCH_SIZE] 
            start = start+BATCH_SIZE

            # wait a second
            time.sleep(1)

        # write task object to database
        task = EmailTask()
        task.started = start_time
        task.finished = timezone.now()
        task.log_text = "\n".join(self.log_lines)
        task.successful = success
        task.email_count = self.success_count
        task.save()

        self.success = success

    def add_log(self, text):
        self.log_lines.append(text)

    def create_invoice_message(self, connection, invoice):
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
            f'Rechnung {invoice.id}.pdf',
            pdfstream.getvalue(),
            'application/pdf')

        return message
