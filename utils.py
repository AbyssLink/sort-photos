import hashlib
import os
import shutil
from datetime import datetime

from PIL import Image
from loguru import logger


@logger.catch
def parse_date_exif(img_file: str):
    """
    extract date info from EXIF data
    code 36867: DateTimeOriginal
    :param img_file:
    :return: datetime
    """
    im = Image.open(img_file)
    exif = im.getexif()
    if exif.get(36867) is not None:
        dt_str = exif.get(36867)
        dt = datetime.strptime(dt_str, '%Y:%m:%d %H:%M:%S')
        return dt
    else:
        return None


def get_file_md5(file: str):
    buf_size = 65536
    md5 = hashlib.md5()
    with open(file, 'rb') as f:
        while True:
            data = f.read(buf_size)
            if not data:
                break
            md5.update(data)
    return md5.hexdigest()


def is_file_duplicate(src_file: str, dst_file: str):
    # todo: finish this function
    if os.path.exists(dst_file):
        if get_file_md5(src_file) == get_file_md5(dst_file):
            logger.warning(
                f'src file = {src_file} is duplicated, will be skipped')
            return True
        else:
            return False
    else:
        return False


def is_dir_valid(dir: str):
    if not os.path.exists(dir):
        logger.error("No Such Directory = ", dir)
        return False
    else:
        return True


def create_dir(dir: str):
    if not os.path.exists(dir):
        os.makedirs(dir)
    else:
        pass
