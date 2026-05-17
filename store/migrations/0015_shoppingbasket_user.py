import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def populate_shoppingbasket_user(apps, schema_editor):
    ShoppingBasket = apps.get_model('store', 'ShoppingBasket')

    unresolved = []

    baskets = ShoppingBasket.objects.select_related('customer__user')

    for basket in baskets:
        if basket.customer_id and basket.customer and basket.customer.user_id:
            basket.user_id = basket.customer.user_id
            basket.save(update_fields=['user'])
        else:
            unresolved.append(str(basket.id))

    if unresolved:
        problems = []
        problems.append('unresolved basket ids: ' + ', '.join(unresolved))
        raise RuntimeError(
            'Could not infer user for all shopping baskets before enforcing non-null user field: '
            + '; '.join(problems)
        )


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_customer_user_fk_reversal'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingbasket',
            name='user',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='shopping_baskets',
                to=settings.AUTH_USER_MODEL,
                verbose_name='User',
            ),
        ),
        migrations.RunPython(populate_shoppingbasket_user, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='shoppingbasket',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='shopping_baskets',
                to=settings.AUTH_USER_MODEL,
                verbose_name='User',
            ),
        ),
    ]
