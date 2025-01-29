from ninja import NinjaAPI, ModelSchema, Field
from typing import List
from depotcommun.models import Article

api = NinjaAPI()


class ArticleSchema(ModelSchema):
    class Meta:
        model = Article
        fields = ['name', 'price']

    group: str = Field(None, alias="group.name")


@api.get("/hello")
def hello(request):
    return "Hello world"


@api.get("/active_articles", response=List[ArticleSchema])
def active_articles(request):
    return Article.objects.filter(active=True)
