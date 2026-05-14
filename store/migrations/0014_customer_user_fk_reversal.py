import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def migrate_forward(apps, schema_editor):
    """Copy existing UserProfile.customer FK data into Customer.user."""
    UserProfile = apps.get_model('store', 'UserProfile')
    for profile in UserProfile.objects.filter(customer__isnull=False):
        profile.customer.user = profile
        profile.customer.save()


def migrate_backward(apps, schema_editor):
    """Restore UserProfile.customer FK from Customer.user."""
    UserProfile = apps.get_model('store', 'UserProfile')
    Customer = apps.get_model('store', 'Customer')
    for customer in Customer.objects.filter(user__isnull=False):
        customer.user.customer = customer
        customer.user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_remove_shoppingbasket_finished_and_more'),
    ]

    operations = [
        # 1. Add the new user FK on Customer (nullable for now)
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='customers',
                to=settings.AUTH_USER_MODEL,
                verbose_name='User',
            ),
        ),
        # 2. Migrate existing FK data
        migrations.RunPython(migrate_forward, migrate_backward),
        # 3. Remove the old customer FK from UserProfile
        migrations.RemoveField(
            model_name='userprofile',
            name='customer',
        ),
    ]
