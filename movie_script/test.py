import urllib.request

url = "http://i3.ytimg.com/vi/J---aiyznGQ/mqdefault.jpg"


result = urllib.request.urlretrieve(
    url, 'D:/Python/Project/Django/MediaServer_V1/movie_script/cat2.jpg')
print()