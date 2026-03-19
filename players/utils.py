import sendgrid
from sendgrid.helpers.mail import Mail
from django.conf import settings


def send_registration_emails(player):

    payment_status = "Paid" if player.payment_status else "Pending"
    transaction_id = getattr(player, "transaction_id", "N/A")

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
                <h2>Hi {player.name},</h2>

                <p>Your registration has been successfully completed ✅</p>

                <h3>🏏 Player Details</h3>
                <p>
                <b>Player ID:</b> {player.player_id} <br>
                <b>Name:</b> {player.name} <br>
                <b>City:</b> {player.city} <br>
                <b>Mobile:</b> {player.mobile} <br>
                <b>Email:</b> {player.email}
                </p>

                <h3>💳 Payment Details</h3>
                <p>
                <b>Status:</b> {payment_status} <br>
                <b>Amount:</b> ₹{player.payment_amount} <br>
                <b>Transaction ID:</b> {transaction_id}
                </p>

                <p>🔥 Thank you for joining ECC Auction Pool!</p>
                <p>You will be notified when auction starts.</p>

                <br>
                <p><b>Elite Cricket Championship</b></p>
                """
            )

            sg.send(message_player)
            print("✅ Player email sent")

        # =========================
        # EMAIL TO ADMIN
        # =========================
        message_admin = Mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_emails=settings.ADMIN_EMAIL,
            subject=f"🚀 New Player Registered - {player.name}",
            html_content=f"""
            <h2>New Player Registration</h2>

            <p><b>Player ID:</b> {player.player_id}</p>
            <p><b>Name:</b> {player.name}</p>
            <p><b>City:</b> {player.city}</p>
            <p><b>Mobile:</b> {player.mobile}</p>
            <p><b>Email:</b> {player.email}</p>

            <h3>Payment Info</h3>
            <p><b>Status:</b> {payment_status}</p>
            <p><b>Amount:</b> ₹{player.payment_amount}</p>
            <p><b>Transaction ID:</b> {transaction_id}</p>

            <br>
            <p>Check admin panel for more details.</p>
            """
        )

        sg.send(message_admin)
        print("✅ Admin email sent")

    except Exception as e:
        print("❌ SendGrid API error:", str(e))