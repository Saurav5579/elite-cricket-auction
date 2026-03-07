from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

# sitemap imports
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from players.models import Player


# correct sitemap config
sitemaps = {
    "players": GenericSitemap({
        "queryset": Player.objects.all(),
    }, priority=0.6)
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("players.urls")),

    # sitemap url
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)