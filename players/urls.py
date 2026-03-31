from django.urls import path
from . import views


urlpatterns = [

    # =========================
    # PAGES
    # =========================
    path("", views.home, name="home"),
    path("register/", views.register_player, name="register_player"),
    path("players/", views.player_list, name="player_list"),

    # ✅ PLAYER DETAIL PAGE (ADD THIS)
    path("player/<int:id>/", views.player_detail, name="player_detail"),
    

    # =========================
    # PAYMENT
    # =========================
    path("payment/<int:player_id>/", views.payment_page, name="payment_page"),
    path("payment-success/<int:player_id>/", views.payment_success, name="payment_success"),


    # =========================
    # 🔥 AUCTION URLS
    # =========================
    path("auction/start/<int:player_id>/", views.start_auction, name="start_auction"),
    path("auction/live/<int:auction_id>/", views.live_auction, name="live_auction"),
    path("auction/bid/<int:auction_id>/", views.place_bid, name="place_bid"),
    path("auction/state/<int:auction_id>/", views.auction_state, name="auction_state"),

    path("export-players/", views.export_players_excel, name="export_players"),
    path("terms/", views.terms, name="terms"),

]