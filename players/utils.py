from django.core.mail import send_mail
from django.conf import settings


def send_registration_emails(player):

    try:
        payment_status = "Paid" if player.payment_status else "Pending"
        transaction_id = player.transaction_id if hasattr(player, "transaction_id") and player.transaction_id else "N/A"

        subject = "🏏 Player Registration Successful - Elite Cricket Championship"

        # =========================
        # EMAIL TO PLAYER
        # =========================

        message_player = f"""
Hello {player.name},

Your player registration has been successfully received.

================================
🏏 PLAYER DETAILS
================================

Player ID      : {player.player_id}
Name           : {player.name}
City           : {player.city}
Mobile         : {player.mobile}
Email          : {player.email}

--------------------------------
Payment Status : {payment_status}
Amount         : ₹{player.payment_amount}
Transaction ID : {transaction_id}

================================

Thank you for registering in the Elite Cricket Championship Auction Pool.

You will be notified once the auction begins.

Regards  
Elite Cricket Championship
"""

        # =========================
        # EMAIL TO ADMIN
        # =========================

        message_admin = f"""
New Player Registration Received

================================
PLAYER DETAILS
================================

Player ID      : {player.player_id}
Name           : {player.name}
City           : {player.city}
Mobile         : {player.mobile}
Email          : {player.email}

--------------------------------
Payment Status : {payment_status}
Amount         : ₹{player.payment_amount}
Transaction ID : {transaction_id}

================================

Please review the player in the admin panel.
"""

        # Send email to Player
        if player.email:
            send_mail(
                subject,
                message_player,
                settings.DEFAULT_FROM_EMAIL,
                [player.email],
                fail_silently=True,
            )

        # Send email to Admin
        send_mail(
            f"New Player Registered - {player.name}",
            message_admin,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=True,
        )

    except Exception as e:
        print("Email error:", e)
        