from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

# Sitemap imports
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from players.models import Player


# Sitemap configuration
info_dict = {
    "players": {
        "queryset": Player.objects.all(),
    }
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("players.urls")),

    # Sitemap URL
    path("sitemap.xml", sitemap, {"sitemaps": info_dict}, name="sitemap"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)