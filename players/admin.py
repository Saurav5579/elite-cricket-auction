from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.utils.html import format_html
from .models import Player, Auction, Team


# ======================
# PLAYER ADMIN
# ======================
@admin.register(Player)
class PlayerAdmin(ImportExportModelAdmin):

    # SERIAL ORDER
    ordering = ("player_id",)

    list_display = (
        "player_id",
        "name",
        "player_photo",   # 🔥 IMAGE COLUMN
        "age",
        "role",
        "city",
        "mobile",
        "base_price",
        "payment_status",
        "is_sold",
    )

    search_fields = (
        "player_id",
        "name",
        "city",
        "mobile",
    )

    list_filter = (
        "role",
        "experience",
        "payment_status",
        "is_sold",
    )

    list_per_page = 25

    # ======================
    # IMAGE PREVIEW 🔥
    # ======================
    def player_photo(self, obj):
        if obj.photo:
            return format_html(
                '<a href="{}" target="_blank">'
                '<img src="{}" width="50" height="50" style="border-radius:6px;" />'
                '</a>',
                obj.photo.url,
                obj.photo.url
            )
        return "No Image"

    player_photo.short_description = "Photo"


# ======================
# AUCTION ADMIN
# ======================
@admin.register(Auction)
class AuctionAdmin(admin.ModelAdmin):

    ordering = ("id",)

    list_display = (
        "id",
        "player",
        "current_price",
        "highest_bidder",
        "is_active",
        "is_closed",
    )

    list_filter = (
        "is_active",
        "is_closed",
    )

    search_fields = (
        "player__name",
        "highest_bidder",
    )


# ======================
# TEAM ADMIN
# ======================
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):

    ordering = ("name",)

    list_display = (
        "name",
        "owner",
        "total_budget",
        "remaining_budget",
    )

    search_fields = (
        "name",
        "owner",
    )