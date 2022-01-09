from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework import generics, permissions
from rest_framework.response import Response

from . import models
from . import permissions as my_permissions
from . import serializers

from .invoice_pdf import InvoicePdfRenderer
from .articles_pdf import ArticlesPdfRenderer


class AvailableItemsView(generics.ListAPIView):
    def get_queryset(self):
        now = timezone.now()
        is_active_query = Q(active_from__lte=now) & (Q(active_until__isnull=True) | Q(active_until__gt=now))

        queryset = models.Article.objects.filter(is_active_query)
        return queryset

    serializer_class = serializers.AvailableItemsSerializer
    permission_classes = [permissions.IsAuthenticated]


class UsersView(generics.ListCreateAPIView):
    def get_queryset(self):
        return models.UserProfile.objects.all()

    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class CurrentUser(generics.GenericAPIView):
    """
    Simple get-only view returning the currently logged in user.
    Is used by frontend to determine authentication state
    """
    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]

@permission_required('store.view_invoice', raise_exception=True)
def invoice_pdf(request, id):
    invoice = get_object_or_404(models.Invoice, pk=id)

    filename = "DC Rechnung %d.pdf" % invoice.id
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = \
        "attachment; filename=\"" + filename + "\""

    InvoicePdfRenderer().render(invoice, response)
    return response


def articles_pdf(request):
    """
    generate pdf of all active articles.
    """
    articles = models.Article.objects.filter(active=True)

    filename = "Artikel Liste"
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = \
        f'attachment; filename="{filename}"'

    ArticlesPdfRenderer().render(articles, response)
    return response

