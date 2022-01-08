from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView


urlpatterns = [
    # entry path redirects to admin
    path('', RedirectView.as_view(url='/admin/', permanent=True)),
    # commented out frontend index.html
    # path('', TemplateView.as_view(template_name='index.html')),
    path('store/', include('store.urls')),
    path('admin/', admin.site.urls),
]
