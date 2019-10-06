import os
import json
import sys
import django

conf_path = os.fspath(
    "D:/Python/Project/Django/MediaServer_V1/movie_script/config.json")

with open(conf_path) as config:
    conf_data = json.load(config)

sys.path.append(conf_data['project_dir'])
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'media_server.settings')

django.setup()
