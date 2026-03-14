import requests
from django.conf import settings


def send_registration_emails(player):

    payment_status = "Paid" if player.payment_status else "Pending"
    transaction_id = player.transaction_id if getattr(player, "transaction_id", None) else "N/A"

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

    try:

        url = "https://api.brevo.com/v3/smtp/email"

        headers = {
            "accept": "application/json",
            "api-key": settings.BREVO_API_KEY,
            "content-type": "application/json"
        }

        # =========================
        # SEND EMAIL TO PLAYER
        # =========================

        if player.email:

            data_player = {
                "sender": {
                    "name": "Elite Cricket Championship",
                    "email": settings.DEFAULT_FROM_EMAIL
                },
                "to": [
                    {
                        "email": player.email
                    }
                ],
                "subject": subject,
                "textContent": message_player
            }

            response_player = requests.post(url, json=data_player, headers=headers)

            print("Player email response:", response_player.status_code, response_player.text)

        # =========================
        # SEND EMAIL TO ADMIN
        # =========================

        data_admin = {
            "sender": {
                "name": "ECC Registration System",
                "email": settings.DEFAULT_FROM_EMAIL
            },
            "to": [
                {
                    "email": settings.ADMIN_EMAIL
                }
            ],
            "subject": f"New Player Registered - {player.name}",
            "textContent": message_admin
        }

        response_admin = requests.post(url, json=data_admin, headers=headers)

        print("Admin email response:", response_admin.status_code, response_admin.text)

        print("Emails sent successfully")

    except Exception as e:
        print("Email sending error:", str(e))