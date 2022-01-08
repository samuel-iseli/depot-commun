from django.core.management.base import BaseCommand
from store.models import Item, ItemGroup

class Command(BaseCommand):
    help = 'create some example data'

    def handle(self, *args, **options):
        self.create_groups()
        self.create_items()

        self.stdout.write(self.style.SUCCESS('Successfully created data'))

    def create_groups(self):
        self.food = ItemGroup.objects.create(
            idx=1,
            name='Food'
        )
        self.sweets = ItemGroup.objects.create(
            idx=2,
            name='Süsses'
        )
        self.unpackaged = ItemGroup.objects.create(
            idx=3,
            name='Unverpackt'
        )
        self.nonfood = ItemGroup.objects.create(
            idx=4,
            name='Non-Food'
        )
        self.beverages = ItemGroup.objects.create(
            idx=5,
            name='Getränke'
        )

    def create_items(self):
        # Food
        self.create_item('Apfelmus bio', 5.0, self.food)
        self.create_item('Apfelmus bio', 5.0, self.food)
        self.create_item('Basilikumsugo', 4.8, self.food)
        self.create_item('Bratöl, Oliven', 11.0, self.food)
        self.create_item('Balsamico', 11.0, self.food)
        self.create_item('Essig', 5.1, self.food)

        self.create_item('Essiggurken', 3.0, self.food)

        self.create_item('Gemüsebouillon', 15.0, self.food)
        self.create_item('Ketchup', 2.5, self.food)
        self.create_item('Kokosmilch', 1.8, self.food)

        self.create_item('Kaffee 500g gemahlen', 13.0, self.food)
        self.create_item('Kaffee 1kg ganz', 25.0, self.food)

        self.create_item('Bulgur', 4.0, self.food)
        self.create_item('Kichererbsen', 4.0, self.food)
        self.create_item('Linsen rot/schwarz', 7.1, self.food)
        self.create_item('Mehl weiss/ruch bio', 3.5, self.food)
        self.create_item('Mehl weiss', 1.5, self.food)

        self.create_item('Milch UHT', 3.5, self.food)

        # Süsses
        self.create_item('Fruchtdessert', 4.5, self.sweets)
        self.create_item('Glace Sorbetto', 3.0, self.sweets)
        self.create_item('Guetzli alle Sorten', 3.5, self.sweets)
        self.create_item('Honig gross', 14.0, self.sweets)
        self.create_item('Honig klein', 8.5, self.sweets)
        self.create_item('Lindt Orange, Excell., Chili', 3.5, self.sweets)
        self.create_item('Lindt Milch', 2.5, self.sweets)
        self.create_item('Maltesers', 1.3, self.sweets)
        self.create_item('Branche Praliné', 1.0, self.sweets)

        # unverpackt
        self.create_item('Basmati gross', 6, self.unpackaged)
        self.create_item('Basmati mittel', 2.9, self.unpackaged)
        self.create_item('Basmati klein', 1.2, self.unpackaged)
        self.create_item('Couscous gross', 6.5, self.unpackaged)
        self.create_item('Couscous mittel', 2.8, self.unpackaged)
        self.create_item('Couscous klein', 1.2, self.unpackaged)


        # Nonfood
        self.create_item('Backtrennpapier', 3.2, self.nonfood)
        self.create_item('Haushaltpapier', 3.5, self.nonfood)
        self.create_item('Regeneriersalz', 1.3, self.nonfood)
        self.create_item('Sonnett Spülglanz', 6.0, self.nonfood)

        # Getränke
        self.create_item('Africola', 2.3, self.beverages)
        self.create_item('Chinotto', 2.0, self.beverages)
        self.create_item('Flauder', 1.5, self.beverages)
        self.create_item('Gazosa', 2.0, self.beverages)
        self.create_item('Bier 3.3dl', 1.7, self.beverages)
        self.create_item('Bier Paul 08', 2.5, self.beverages)
        self.create_item('Al Muvedre bio', 11.0, self.beverages)
        self.create_item('Arriezu', 13.0, self.beverages)
        self.create_item('Chardonnay', 13.0, self.beverages)

    def create_item(self, name, price, group):
        item = Item(
            name=name, price=price,
            group=group)
        item.save()

        return item
