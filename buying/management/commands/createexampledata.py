from django.core.management.base import BaseCommand
from buying.models import Depot, Item, UserProfile, ItemGroup


class Command(BaseCommand):
    help = 'create some example data'

    def handle(self, *args, **options):
        self.depot = self.get_or_create_depot('Heizenholz', 'Heizenholz')

        self.create_groups()
        self.create_items()

        self.stdout.write(self.style.SUCCESS('Successfully created data'))

    def create_groups(self):
        self.conserves = ItemGroup.objects.create(
            idx=10,
            name='Konserven'
        )
        self.grains = ItemGroup.objects.create(
            idx=20,
            name='Getreide / Hülsenfrüchte'
        )
        self.sweets = ItemGroup.objects.create(
            idx=30,
            name='Süsses'
        )
        self.beverages = ItemGroup.objects.create(
            idx=40,
            name='Getränke'
        )
        self.nonfood = ItemGroup.objects.create(
            idx=50,
            name='Non-Food'
        )

    def create_items(self):
        # Konserven
        self.create_item(100, 'Apfelmus bio', 6.0, self.conserves)
        self.create_item(110, 'Basilikumsugo', 4.8, self.conserves)
        self.create_item(120, 'Bratöl, Oliven', 11.0, self.conserves)
        self.create_item(121, 'Balsamico', 11.0, self.conserves)
        self.create_item(122, 'Essig', 5.1, self.conserves)

        self.create_item(130, 'Essiggurken', 3.0, self.conserves)

        self.create_item(140, 'Gemüsebouillon', 15.0, self.conserves)
        self.create_item(141, 'Ketchup', 2.5, self.conserves)
        self.create_item(142, 'Kokosmilch', 1.8, self.conserves)

        self.create_item(150, 'Kaffee 500g gemahlen', 13.0, self.conserves)
        self.create_item(151, 'Kaffee 1kg ganz', 25.0, self.conserves)

        # Getreide
        self.create_item(200, 'Bulgur', 4.0, self.grains)
        self.create_item(201, 'Kichererbsen', 4.0, self.grains)
        self.create_item(202, 'Linsen rot/schwarz', 7.1, self.grains)
        self.create_item(203, 'Mehl weiss/ruch bio', 3.5, self.grains)
        self.create_item(204, 'Mehl weiss', 1.5, self.grains)

        self.create_item(210, 'Milch UHT', 3.5, self.grains)

        # Süsses
        self.create_item(301, 'Fruchtdessert', 4.5, self.sweets)
        self.create_item(302, 'Glace Sorbetto', 3.0, self.sweets)
        self.create_item(303, 'Guetzli alle Sorten', 3.5, self.sweets)
        self.create_item(310, 'Honig gross', 14.0, self.sweets)
        self.create_item(311, 'Honig klein', 8.5, self.sweets)
        self.create_item(320, 'Lindt Orange, Excell., Chili', 3.5, self.sweets)
        self.create_item(321, 'Lindt Milch', 2.5, self.sweets)
        self.create_item(322, 'Maltesers', 1.3, self.sweets)
        self.create_item(323, 'Branche Praliné', 1.0, self.sweets)

        # Nonfood
        self.create_item(400, 'Backtrennpapier', 3.2, self.nonfood)
        self.create_item(401, 'Haushaltpapier', 3.5, self.nonfood)
        self.create_item(402, 'Regeneriersalz', 1.3, self.nonfood)
        self.create_item(403, 'Sonnett Spülglanz', 6.0, self.nonfood)

        # Getränke
        self.create_item(500, 'Africola', 2.3, self.beverages)
        self.create_item(501, 'Chinotto', 2.0, self.beverages)
        self.create_item(502, 'Flauder', 1.5, self.beverages)
        self.create_item(503, 'Gazosa', 2.0, self.beverages)
        self.create_item(510, 'Bier 3.3dl', 1.7, self.beverages)
        self.create_item(511, 'Bier Paul 08', 2.5, self.beverages)
        self.create_item(520, 'Al Muvedre bio', 11.0, self.beverages)
        self.create_item(521, 'Arriezu', 13.0, self.beverages)
        self.create_item(522, 'Chardonnay', 13.0, self.beverages)

    def get_or_create_depot(self, name, location):
        depots = Depot.objects.all()
        if len(depots) > 0:
            return depots[0]

        depot = Depot(name=name, location=location)
        users = UserProfile.objects.all()
        for user in users:
            user.depot = depot
        depot.save()
        return depot

    def create_item(self, number, name, price, group):
        item = Item(
            code=number, name=name, price=price,
            depot=self.depot,
            group=group)
        item.save()

        return item
