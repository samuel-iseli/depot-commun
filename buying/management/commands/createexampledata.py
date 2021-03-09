from django.core.management.base import BaseCommand
from buying.models import Depot, Item, UserProfile, Tag


class Command(BaseCommand):
    help = 'create some example data'

    def handle(self, *args, **options):
        self.depot = self.get_or_create_depot('Heizenholz', 'Heizenholz')

        self.create_items()

        self.stdout.write(self.style.SUCCESS('Successfully created data'))

    def create_items(self):
        # Konserven
        self.create_item(100, 'Apfelmus bio', 6.0, 'Konserven')
        self.create_item(110, 'Basilikumsugo', 4.8, 'Konserven')
        self.create_item(120, 'Bratöl, Oliven', 11.0, 'Konserven')
        self.create_item(121, 'Balsamico', 11.0, 'Konserven')
        self.create_item(122, 'Essig', 5.1, 'Konserven')

        self.create_item(130, 'Essiggurken', 3.0, 'Konserven')

        self.create_item(140, 'Gemüsebouillon', 15.0, 'Konserven')
        self.create_item(141, 'Ketchup', 2.5, 'Konserven')
        self.create_item(142, 'Kokosmilch', 1.8, 'Konserven')

        self.create_item(150, 'Kaffee 500g gemahlen', 13.0, 'Konserven')
        self.create_item(151, 'Kaffee 1kg ganz', 25.0, 'Konserven')

        # Getreide
        self.create_item(200, 'Bulgur', 4.0, 'Getreide/Hülsenfrüchte')
        self.create_item(201, 'Kichererbsen', 4.0, 'Getreide/Hülsenfrüchte')
        self.create_item(202, 'Linsen rot/schwarz', 7.1, 'Getreide/Hülsenfrüchte')
        self.create_item(203, 'Mehl weiss/ruch bio', 3.5, 'Getreide/Hülsenfrüchte')
        self.create_item(204, 'Mehl weiss', 1.5, 'Getreide/Hülsenfrüchte')

        self.create_item(210, 'Milch UHT', 3.5, 'Getreide/Hülsenfrüchte')

        # Süsses
        self.create_item(301, 'Fruchtdessert', 4.5, 'Süsses')
        self.create_item(302, 'Glace Sorbetto', 3.0, 'Süsses')
        self.create_item(303, 'Guetzli alle Sorten', 3.5, 'Süsses')
        self.create_item(310, 'Honig gross', 14.0, 'Süsses')
        self.create_item(311, 'Honig klein', 8.5, 'Süsses')
        self.create_item(320, 'Lindt Orange, Excell., Chili', 3.5, 'Süsses')
        self.create_item(321, 'Lindt Milch', 2.5, 'Süsses')
        self.create_item(322, 'Maltesers', 1.3, 'Süsses')
        self.create_item(323, 'Branche Praliné', 1.0, 'Süsses')

        # Nonfood
        self.create_item(400, 'Backtrennpapier', 3.2, 'Nonfood')
        self.create_item(401, 'Haushaltpapier', 3.5, 'Nonfood')
        self.create_item(402, 'Regeneriersalz', 1.3, 'Nonfood')
        self.create_item(403, 'Sonnett Spülglanz', 6.0, 'Nonfood')

        # Getränke
        self.create_item(500, 'Africola', 2.3, 'Getränke')
        self.create_item(501, 'Chinotto', 2.0, 'Getränke')
        self.create_item(502, 'Flauder', 1.5, 'Getränke')
        self.create_item(503, 'Gazosa', 2.0, 'Getränke')
        self.create_item(510, 'Bier 3.3dl', 1.7, 'Getränke')
        self.create_item(511, 'Bier Paul 08', 2.5, 'Getränke')
        self.create_item(520, 'Al Muvedre bio', 11.0, 'Getränke')
        self.create_item(521, 'Arriezu', 13.0, 'Getränke')
        self.create_item(522, 'Chardonnay', 13.0, 'Getränke')

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

    def create_item(self, number, name, price, category):
        item = Item(product_nr=number, name=name, price=price)
        item.depot = self.depot
        item.save()

        categories = Tag.objects.filter(name=category)
        if len(categories) > 0:
            cat = categories[0]
        else:
            cat = Tag.objects.create(name=category)
            cat.save()

        item.tags.add(cat)
        item.save()
        return item
