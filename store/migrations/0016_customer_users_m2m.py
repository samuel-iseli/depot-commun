from django.conf import settings
from django.db import migrations, models


def migrate_customer_user_fk_to_m2m(apps, schema_editor):
    Customer = apps.get_model('store', 'Customer')

    for customer in Customer.objects.exclude(user__isnull=True):
        customer.users.add(customer.user_id)


def migrate_customer_user_m2m_to_fk(apps, schema_editor):
    Customer = apps.get_model('store', 'Customer')

    for customer in Customer.objects.all():
        user = customer.users.order_by('id').first()
        customer.user = user
        customer.save(update_fields=['user'])


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_shoppingbasket_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='users',
            field=models.ManyToManyField(
                blank=True,
                related_name='customers',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Users',
            ),
        ),
        migrations.RunPython(migrate_customer_user_fk_to_m2m, migrate_customer_user_m2m_to_fk),
        migrations.RemoveField(
            model_name='customer',
            name='user',
        ),
    ]
