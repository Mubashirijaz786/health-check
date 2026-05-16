from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('favicon.ico', RedirectView.as_view(url='/static/medical_dashboard_illustration.png')), # Redirect to an existing image
    path('', include('core.urls')),
]
