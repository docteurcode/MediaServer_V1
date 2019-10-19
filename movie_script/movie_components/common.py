from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.request import urlopen


def get_tmp_image(image_url):
    # Phot Download
    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(urlopen(image_url).read())
    img_temp.flush()
    return img_temp


def inside_folders(name):
    folders = Path(name).glob("*")
    folders_array = [folder for folder in folders]
    return folders_array


def get_file(file_full_path, folder_path):
    dir_split_by = folder_path.split("/")[-2]
    str_full_path = str(file_full_path).replace("\\", "/")
    file_path = str_full_path.split(dir_split_by)[-1]
    return file_path
