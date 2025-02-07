from ninja import NinjaAPI, Schema, ModelSchema, Field
from typing import List
from depotcommun.models import Article, Purchase, ShoppingBasket
from datetime import datetime

api = NinjaAPI()


class ArticleSchema(ModelSchema):
    class Meta:
        model = Article
        fields = ['name', 'price', 'id']

    group: str = Field(None, alias="group.name")


@api.get("/hello")
def hello(request):
    return "Hello world"


@api.get("/active_articles", response=List[ArticleSchema])
def active_articles(request):
    return Article.objects.filter(active=True)


class PurchaseIn(Schema):
    article_id: int
    quantity: int
    price: float = None


class ShoppingBasketIn(Schema):
    date: datetime = None
    customer_id: int
    purchases: List[PurchaseIn]


@api.post("/shopping_baskets")
def create_basket(request, payload: ShoppingBasketIn):
    # create a new shopping basket
    basket = ShoppingBasket.objects.create(
        date=payload.date,
        customer_id=payload.customer_id
    )
    basket.save()

    for purchase in payload.purchases:
        purchase_obj = Purchase.objects.create(
            basket=basket,
            article_id=purchase.article_id,
            quantity=purchase.quantity,
            price=purchase.price
        )
        purchase_obj.save()
