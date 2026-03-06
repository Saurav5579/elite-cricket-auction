from django.db import models
from django.utils import timezone


class Player(models.Model):

    ROLE_CHOICES = [
        ("Batsman", "Batsman"),
        ("Bowler", "Bowler"),
        ("All-Rounder", "All-Rounder"),
        ("Wicket-Keeper", "Wicket-Keeper"),
    ]

    EXPERIENCE_CHOICES = [
        ("Beginner", "Beginner"),
        ("Intermediate", "Intermediate"),
        ("Professional", "Professional"),
    ]

    STYLE_CHOICES = [
        ("Right-Hand", "Right-Hand"),
        ("Left-Hand", "Left-Hand"),
        ("Fast Bowler", "Fast Bowler"),
        ("Spin Bowler", "Spin Bowler"),
    ]

    # ✅ Auto Player ID
    player_id = models.CharField(max_length=10, unique=True, blank=True)

    # ✅ Basic Details
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    city = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        blank=True,
        null=True
    )

    playing_style = models.CharField(
        max_length=30,
        choices=STYLE_CHOICES,
        blank=True,
        null=True
    )

    experience = models.CharField(
        max_length=30,
        choices=EXPERIENCE_CHOICES,
        blank=True,
        null=True
    )

    base_price = models.IntegerField(default=500)

    # ✅ Uploads
    photo = models.ImageField(
        upload_to="players/photos/",
        blank=True,
        null=True
    )

    document = models.FileField(
        upload_to="players/docs/",
        blank=True,
        null=True
    )

    # ✅ Terms Checkbox
    agreed_terms = models.BooleanField(default=False)

    # =========================
    # PAYMENT DETAILS
    # =========================
    payment_status = models.BooleanField(default=False)
    payment_amount = models.IntegerField(default=1000)

    payment_date = models.DateTimeField(blank=True, null=True)

    # ⭐ NEW FIELD (Transaction ID)
    transaction_id = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    # =========================
    # AUCTION STATUS
    # =========================
    is_sold = models.BooleanField(default=False)
    sold_price = models.IntegerField(blank=True, null=True)

    # =========================
    # AUTO PLAYER ID GENERATOR
    # =========================
    def save(self, *args, **kwargs):
        if not self.player_id:
            last_player = Player.objects.order_by("id").last()

            if last_player and last_player.player_id:
                last_number = int(last_player.player_id[1:])
                new_number = last_number + 1
            else:
                new_number = 1

            self.player_id = f"P{new_number:03d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.player_id} - {self.name}"


# =========================
# AUCTION MODEL
# =========================
class Auction(models.Model):

    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    current_price = models.IntegerField(default=0)
    highest_bidder = models.CharField(max_length=100, blank=True)

    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return f"Auction - {self.player.name}"


# =========================
# TEAM MODEL
# =========================
class Team(models.Model):

    name = models.CharField(max_length=100, unique=True)
    owner = models.CharField(max_length=100, blank=True, null=True)

    total_budget = models.IntegerField(default=50000)
    remaining_budget = models.IntegerField(default=50000)

    logo = models.ImageField(
        upload_to="teams/logo/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


# =========================
# BID MODEL
# =========================
class Bid(models.Model):

    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bidder = models.CharField(max_length=100)

    amount = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder} - {self.amount}"


# =========================
# SITE SETTINGS
# =========================
class SiteSetting(models.Model):

    auction_enabled = models.BooleanField(default=False)

    auction_start_time = models.DateTimeField(
        null=True,
        blank=True
    )

    maintenance_mode = models.BooleanField(default=False)

    def __str__(self):
        return "Site Control Settings"