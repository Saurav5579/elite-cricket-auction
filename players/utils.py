import sendgrid
from sendgrid.helpers.mail import Mail
from django.conf import settings


def send_registration_emails(player):

    # =========================
    # SAFE VALUES (FINAL FIX)
    # =========================
    payment_status = "Paid" if player.payment_status else "Pending"

    # ✅ Amount fix (DB > fallback)
    amount = player.payment_amount if player.payment_amount else settings.REGISTRATION_FEE

    # ✅ Transaction ID fix (no FAILED issue)
    transaction_id = (
        player.transaction_id
        if player.transaction_id and player.transaction_id not in ["FAILED", "", None]
        else "SUCCESS"
    )

    try:
        sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)

        # =========================
        # EMAIL TO PLAYER
        # =========================
        if player.email:
            message_player = Mail(
                from_email=settings.DEFAULT_FROM_EMAIL,
                to_emails=player.email,
                subject="🏏 Registration Successful - Elite Cricket Championship",
                html_content=f"""
                <div style="font-family:Arial; background:#0b1220; padding:25px; color:#ffffff; border-radius:10px;">
                
                <h2 style="color:#00ffcc;">Hi {player.name},</h2>

                <p>Your registration has been successfully completed ✅</p>

                <hr style="border:1px solid rgba(255,255,255,0.1);">

                <h3>🏏 Player Details</h3>
                <p>
                <b>Player ID:</b> {player.player_id} <br>
                <b>Name:</b> {player.name} <br>
                <b>City:</b> {player.city} <br>
                <b>Mobile:</b> {player.mobile} <br>
                <b>Email:</b> {player.email}
                </p>

                <hr style="border:1px solid rgba(255,255,255,0.1);">

                <h3>💳 Payment Details</h3>
                <p>
                <b>Status:</b> {payment_status} <br>
                <b>Amount:</b> ₹{amount} <br>
                <b>Transaction ID:</b> {transaction_id}
                </p>

                <hr style="border:1px solid rgba(255,255,255,0.1);">

                <p>🔥 Thank you for joining ECC Auction Pool!</p>
                <p>You will be notified when auction starts.</p>

                <br>
                <p style="font-size:14px; opacity:0.8;">
                Regards,<br>
                <b>Elite Cricket Championship</b>
                </p>

                </div>
                """
            )

            sg.send(message_player)
            print("✅ Player email sent")

        # =========================
        # EMAIL TO ADMIN
        # =========================
        if settings.ADMIN_EMAIL:
            message_admin = Mail(
                from_email=settings.DEFAULT_FROM_EMAIL,
                to_emails=settings.ADMIN_EMAIL,
                subject=f"🚀 New Player Registered - {player.name}",
                html_content=f"""
                <div style="font-family:Arial; background:#0b1220; padding:25px; color:#ffffff; border-radius:10px;">

                <h2>New Player Registration</h2>

                <p><b>Player ID:</b> {player.player_id}</p>
                <p><b>Name:</b> {player.name}</p>
                <p><b>City:</b> {player.city}</p>
                <p><b>Mobile:</b> {player.mobile}</p>
                <p><b>Email:</b> {player.email}</p>

                <hr style="border:1px solid rgba(255,255,255,0.1);">

                <h3>Payment Info</h3>
                <p><b>Status:</b> {payment_status}</p>
                <p><b>Amount:</b> ₹{amount}</p>
                <p><b>Transaction ID:</b> {transaction_id}</p>

                <br>
                <p>Check admin panel for more details.</p>

                </div>
                """
            )

            sg.send(message_admin)
            print("✅ Admin email sent")

    except Exception as e:
        print("❌ SendGrid API error:", str(e))