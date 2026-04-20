from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Article


@login_required
def home(request):
    return render(request, 'store/home.html')


@login_required
def new_purchase(request):
    return render(request, 'store/purchase.html')

@login_required
def add_article(request):
    articles = Article.objects.all()
    return render(request, 'store/article_detail.html', {'articles': articles})
