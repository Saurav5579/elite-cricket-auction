from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
import razorpay

from .models import Player, Auction, Bid
from .forms import PlayerForm
import razorpay

from django.shortcuts import render, get_object_or_404
from .models import Player

# =========================
# HOME PAGE
# =========================
def home(request):
    return render(request, "players/home.html")


# =========================
# PLAYER REGISTER
# =========================
def register_player(request):

    if request.method == "POST":

        form = PlayerForm(request.POST, request.FILES)

        mobile = request.POST.get("mobile")
        email = request.POST.get("email")

        # Duplicate Mobile Check
        if Player.objects.filter(mobile=mobile).exists():
            return render(request, "players/register.html", {
                "form": form,
                "error": "This mobile number is already registered!"
            })

        # Duplicate Email Check
        if Player.objects.filter(email=email).exists():
            return render(request, "players/register.html", {
                "form": form,
                "error": "This email is already registered!"
            })

        if form.is_valid():

            player = form.save(commit=False)

            player.payment_status = False

            player.save()

            return redirect("payment_page", player_id=player.id)

    else:
        form = PlayerForm()

    return render(request, "players/register.html", {"form": form})

# =========================
# PAYMENT PAGE (Direct Razorpay Popup)
# =========================

import razorpay
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.utils import timezone
from .models import Player
from .utils import send_registration_emails


def payment_page(request, player_id):

    player = get_object_or_404(Player, id=player_id)

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    amount = int(player.payment_amount * 100)

    order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"
    })

    context = {
        "player": player,
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "amount": amount,
        "order_id": order["id"]
    }

    return render(request, "players/payment.html", context)


# =========================
# PAYMENT SUCCESS (FINAL SAFE VERSION)
# =========================

def payment_success(request, player_id):

    player = get_object_or_404(Player, id=player_id)

    razorpay_order_id = request.GET.get("razorpay_order_id")
    razorpay_payment_id = request.GET.get("razorpay_payment_id")
    razorpay_signature = request.GET.get("razorpay_signature")

    error_message = None

    try:
        # =========================
        # VERIFY PAYMENT (OPTIONAL / SAFE)
        # =========================
        if razorpay_order_id and razorpay_payment_id and razorpay_signature:
            try:
                client = razorpay.Client(
                    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
                )

                client.utility.verify_payment_signature({
                    "razorpay_order_id": razorpay_order_id,
                    "razorpay_payment_id": razorpay_payment_id,
                    "razorpay_signature": razorpay_signature
                })

                print("✅ Payment verified")

            except Exception as verify_error:
                print("⚠️ Verification skipped:", verify_error)
                error_message = "Verification skipped (test mode)"

        else:
            print("⚠️ Missing Razorpay params")

        # =========================
        # SAVE PAYMENT (ONLY ONCE)
        # =========================
        if not player.payment_status:
            player.payment_status = True
            player.payment_date = timezone.now()
            player.transaction_id = razorpay_payment_id or "TEST_PAYMENT"
            player.save()

            print("✅ Payment saved")

            # =========================
            # SEND EMAIL (API BASED)
            # =========================
            try:
                send_registration_emails(player)
                print("✅ Email sent successfully")
            except Exception as email_error:
                print("❌ Email error:", email_error)

        else:
            print("⚠️ Payment already processed")

    except Exception as e:
        print("❌ Unexpected error:", e)
        error_message = "Something went wrong, but registration saved."

    # =========================
    # ALWAYS SHOW SUCCESS PAGE
    # =========================
    return render(request, "players/payment_success.html", {
        "player": player,
        "error": error_message
    })
# =========================
# PLAYER LIST
# =========================
from .models import SiteSetting

def player_list(request):
    players = Player.objects.all().order_by("player_id")
    settings_obj = SiteSetting.objects.first()

    return render(request, "players/player_list.html", {
        "players": players,
        "settings_obj": settings_obj
    })


# =========================
# START AUCTION
# =========================
def start_auction(request, player_id):

    if not getattr(settings, "AUCTION_ENABLED", False):
        return redirect("player_list")

    player = get_object_or_404(Player, id=player_id)

    if not player.payment_status:
        return redirect("payment_page", player_id=player.id)

    active = Auction.objects.filter(is_active=True).first()

    if active:
        if timezone.now() > active.end_time:
            active.is_active = False
            active.is_closed = True
            active.save()
        else:
            return redirect("live_auction", auction_id=active.id)

    auction = Auction.objects.create(
        player=player,
        current_price=player.base_price,
        start_time=timezone.now(),
        end_time=timezone.now() + timedelta(seconds=60),
        is_active=True,
        is_closed=False
    )

    return redirect("live_auction", auction_id=auction.id)


# =========================
# LIVE AUCTION PAGE
# =========================
def live_auction(request, auction_id):

    auction = get_object_or_404(Auction, id=auction_id)

    if auction.is_active and timezone.now() > auction.end_time:

        auction.is_active = False
        auction.is_closed = True

        if auction.highest_bidder:
            auction.player.is_sold = True
            auction.player.sold_price = auction.current_price
            auction.player.save()

        auction.save()

    return render(request, "auction/live.html", {"auction": auction})


# =========================
# PLACE BID (AJAX)
# =========================
def place_bid(request, auction_id):

    if request.method != "POST":
        return JsonResponse({"status": "error"})

    auction = get_object_or_404(Auction, id=auction_id)

    if not auction.is_active:
        return JsonResponse({"status": "closed"})

    try:
        amount = int(request.POST.get("amount", 0))
    except ValueError:
        return JsonResponse({"status": "bad_amount"})

    bidder = request.POST.get("bidder", "Guest")

    if amount > auction.current_price:

        auction.current_price = amount
        auction.highest_bidder = bidder
        auction.save()

        Bid.objects.create(
            auction=auction,
            bidder=bidder,
            amount=amount
        )

        return JsonResponse({
            "status": "ok",
            "price": amount,
            "bidder": bidder
        })

    return JsonResponse({"status": "low"})


# =========================
# REALTIME STATE API
# =========================
def auction_state(request, auction_id):

    auction = get_object_or_404(Auction, id=auction_id)

    bids = Bid.objects.filter(auction=auction).order_by("-time")[:5]

    bid_list = [
        {
            "bidder": b.bidder,
            "amount": b.amount
        }
        for b in bids
    ]

    return JsonResponse({
        "price": auction.current_price,
        "bidder": auction.highest_bidder,
        "active": auction.is_active,
        "bids": bid_list
    })


# =========================
# EXPORT PLAYERS TO EXCEL
# =========================

import openpyxl
from django.http import HttpResponse
from openpyxl.styles import Font, PatternFill, Alignment
from django.contrib.auth.decorators import login_required
from .models import Player


@login_required
def export_players_excel(request):

    if not request.user.is_superuser:
        return HttpResponse("Access Denied")

    players = Player.objects.all().order_by("player_id")

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Registered Players"

    headers = [
        "Player ID",
        "Name",
        "Age",
        "City",
        "Mobile",
        "Email",
        "Role",
        "Playing Style",
        "Experience",
        "Base Price",
        "Payment Status",
        "Transaction ID",
        "Payment Date"
    ]

    sheet.append(headers)

    # Header style
    header_fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF")

    for col in range(1, len(headers) + 1):
        cell = sheet.cell(row=1, column=col)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center")

    # Status colors
    paid_fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
    pending_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")

    row_num = 2

    for player in players:

        payment_status = "Paid" if player.payment_status else "Pending"

        sheet.append([
            player.player_id,
            player.name,
            player.age,
            player.city,
            player.mobile,
            player.email,
            player.role,
            player.playing_style,
            player.experience,
            player.base_price,
            payment_status,
            player.transaction_id if hasattr(player, "transaction_id") and player.transaction_id else "",
            str(player.payment_date) if player.payment_date else ""
        ])

        status_cell = sheet.cell(row=row_num, column=11)

        if payment_status == "Paid":
            status_cell.fill = paid_fill
        else:
            status_cell.fill = pending_fill

        row_num += 1

    # Auto column width
    for column in sheet.columns:
        max_length = 0
        column_letter = column[0].column_letter

        for cell in column:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))

        sheet.column_dimensions[column_letter].width = max_length + 4

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = "attachment; filename=players.xlsx"

    workbook.save(response)

    return response

def terms(request):
    return render(request, "players/terms.html")



def player_detail(request, id):
    from .models import Player
    from django.shortcuts import render, get_object_or_404

    player = get_object_or_404(Player, id=id)

    return render(request, "players/player_detail.html", {
        "player": player
    })

