import os
import sys
import django

sys.path.append("D:/Python/Project/Django/MediaServer_V1")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'media_server.settings')

django.setup()

abir = 'Hello Abir'