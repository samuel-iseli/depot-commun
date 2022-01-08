from django.core.management.base import BaseCommand
from store.models import Article, ArticleGroup

class Command(BaseCommand):
    help = 'create some example data'

    def handle(self, *args, **options):
        self.create_groups()
        self.create_articles()

        self.stdout.write(self.style.SUCCESS('Successfully created data'))

    def create_groups(self):
        self.food = ArticleGroup.objects.create(
            idx=1,
            name='Food'
        )
        self.sweets = ArticleGroup.objects.create(
            idx=2,
            name='Süsses'
        )
        self.unpackaged = ArticleGroup.objects.create(
            idx=3,
            name='Unverpackt'
        )
        self.nonfood = ArticleGroup.objects.create(
            idx=4,
            name='Non-Food'
        )
        self.beverages = ArticleGroup.objects.create(
            idx=5,
            name='Getränke'
        )

    def create_articles(self):
        # Food
        self.create_article('Apfelmus bio', 5.0, self.food)
        self.create_article('Apfelmus bio', 5.0, self.food)
        self.create_article('Basilikumsugo', 4.8, self.food)
        self.create_article('Bratöl, Oliven', 11.0, self.food)
        self.create_article('Balsamico', 11.0, self.food)
        self.create_article('Essig', 5.1, self.food)

        self.create_article('Essiggurken', 3.0, self.food)

        self.create_article('Gemüsebouillon', 15.0, self.food)
        self.create_article('Ketchup', 2.5, self.food)
        self.create_article('Kokosmilch', 1.8, self.food)

        self.create_article('Kaffee 500g gemahlen', 13.0, self.food)
        self.create_article('Kaffee 1kg ganz', 25.0, self.food)

        self.create_article('Bulgur', 4.0, self.food)
        self.create_article('Kichererbsen', 4.0, self.food)
        self.create_article('Linsen rot/schwarz', 7.1, self.food)
        self.create_article('Mehl weiss/ruch bio', 3.5, self.food)
        self.create_article('Mehl weiss', 1.5, self.food)

        self.create_article('Milch UHT', 3.5, self.food)

        # Süsses
        self.create_article('Fruchtdessert', 4.5, self.sweets)
        self.create_article('Glace Sorbetto', 3.0, self.sweets)
        self.create_article('Guetzli alle Sorten', 3.5, self.sweets)
        self.create_article('Honig gross', 14.0, self.sweets)
        self.create_article('Honig klein', 8.5, self.sweets)
        self.create_article('Lindt Orange, Excell., Chili', 3.5, self.sweets)
        self.create_article('Lindt Milch', 2.5, self.sweets)
        self.create_article('Maltesers', 1.3, self.sweets)
        self.create_article('Branche Praliné', 1.0, self.sweets)

        # unverpackt
        self.create_article('Basmati gross', 6, self.unpackaged)
        self.create_article('Basmati mittel', 2.9, self.unpackaged)
        self.create_article('Basmati klein', 1.2, self.unpackaged)
        self.create_article('Couscous gross', 6.5, self.unpackaged)
        self.create_article('Couscous mittel', 2.8, self.unpackaged)
        self.create_article('Couscous klein', 1.2, self.unpackaged)


        # Nonfood
        self.create_article('Backtrennpapier', 3.2, self.nonfood)
        self.create_article('Haushaltpapier', 3.5, self.nonfood)
        self.create_article('Regeneriersalz', 1.3, self.nonfood)
        self.create_article('Sonnett Spülglanz', 6.0, self.nonfood)

        # Getränke
        self.create_article('Africola', 2.3, self.beverages)
        self.create_article('Chinotto', 2.0, self.beverages)
        self.create_article('Flauder', 1.5, self.beverages)
        self.create_article('Gazosa', 2.0, self.beverages)
        self.create_article('Bier 3.3dl', 1.7, self.beverages, 1)
        self.create_article('Bier Paul 08', 2.5, self.beverages, 1)
        self.create_article('Al Muvedre bio', 11.0, self.beverages, 2)
        self.create_article('Arriezu', 13.0, self.beverages, 2)
        self.create_article('Chardonnay', 13.0, self.beverages, 2)

    def create_article(self, name, price, group, sortidx=0):
        article = Article(
            name=name, price=price,
            group=group, sortidx=sortidx)
        article.save()

        return article
