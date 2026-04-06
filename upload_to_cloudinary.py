from players.models import Player
from django.core.files import File
import os

success = 0
failed = 0

for player in Player.objects.all():
    # PHOTO
    if player.photo:
        try:
            path = player.photo.path
            if os.path.exists(path):
                with open(path, 'rb') as f:
                    player.photo.save(os.path.basename(path), File(f), save=True)
                    success += 1
        except Exception as e:
            print("Photo error:", player.name, e)
            failed += 1

    # DOCUMENT
    if player.document:
        try:
            path = player.document.path
            if os.path.exists(path):
                with open(path, 'rb') as f:
                    player.document.save(os.path.basename(path), File(f), save=True)
                    success += 1
        except Exception as e:
            print("Doc error:", player.name, e)
            failed += 1

print("Upload Completed")
print("Success:", success)
print("Failed:", failed)