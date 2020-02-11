import os
import shutil
import time
from datetime import datetime

from PIL import Image
from loguru import logger

base_path = '/Users/chiya/Pictures/Sorting/Unsort'
write_path = '/Users/chiya/Pictures/Sorting/Photos_Collection'
src_img_num = 0
dst_img_num = 0
un_tag_num = 0
name_cnt_dict = {}


def sort_img(base_name_, file_path_):
    global dst_img_num, un_tag_num
    month = get_month(file_path_)
    if month is not None:
        # add 0 if single digit
        month = f'{int(month):02}'
        year = get_year(file_path_)
        if not os.path.exists(os.path.join(write_path, year, month)):
            os.makedirs(os.path.join(write_path, year, month))
        copy_path = os.path.join(
            os.path.join(write_path, year, month), base_name_)
        shutil.copy(file_path_, copy_path)
        update_img_name(copy_path)
    else:
        if not os.path.exists(os.path.join(write_path, "unknown")):
            os.makedirs(os.path.join(write_path, "unknown"))
        divisor = un_tag_num // 300
        if not os.path.exists(os.path.join(write_path, "unknown", str(divisor))):
            os.makedirs(os.path.join(write_path, "unknown", str(divisor)))
        copy_path = os.path.join(
            os.path.join(write_path, "unknown", str(divisor)), base_name_)
        shutil.copy(file_path_, copy_path)
        update_img_name(copy_path)


def main_process(path_):
    global src_img_num
    files = os.listdir(path_)
    for file in files:
        if not file.startswith('.'):
            file_path = os.path.join(path_, file)
            if os.path.isfile(file_path):
                types = [".jpeg", ".jpg", ".png"]
                extension = os.path.splitext(file)[1]
                if extension in types:
                    src_img_num = src_img_num + 1
                    sort_img(base_name_=file, file_path_=file_path)
                else:
                    continue
            else:
                main_process(file_path)
        else:
            continue


@logger.catch
def get_original_time(img_path_: str):
    # png don't contain exif info
    types = [".png"]
    ext_name = os.path.splitext(img_path_)[1]
    if ext_name in types:
        return None
    im = Image.open(img_path_)
    exif = im.getexif()
    if exif.get(36867) is not None:
        dt_str = exif.get(36867)
        # print(dt_str)
        try:
            dt = datetime.strptime(dt_str, '%Y:%m:%d %H:%M:%S')
            return dt
        except:
            print("An error in Date, file path = ", img_path_)
    else:
        return None


def get_month(img_path_: str):
    dt = get_original_time(img_path_)
    if dt is not None:
        return str(dt.month)
    else:
        return None


def get_year(img_path_: str):
    dt = get_original_time(img_path_)
    if dt is not None:
        return str(dt.year)
    else:
        return None


def update_img_name(img_path_: str):
    global un_tag_num, dst_img_num, name_cnt_dict
    dt = get_original_time(img_path_)
    ext_name = os.path.splitext(img_path_)[1]
    if dt is None:
        mtime = os.path.getmtime(img_path_)
        dt = datetime.fromtimestamp(mtime)
        dt_str = dt.strftime('%m-%d-%Y (%H%M%S)') + '_' + str(un_tag_num)
        un_tag_num = un_tag_num + 1
    else:
        dt_str = dt.strftime('%m-%d-%Y (%H%M%S)')
    new_basename = dt_str + ext_name
    dirname = os.path.dirname(img_path_)
    new_path = os.path.join(dirname, new_basename)
    if os.path.exists(new_path):
        if new_basename in name_cnt_dict.keys():
            name_cnt_dict[new_basename] = name_cnt_dict[new_basename] + 1
        else:
            name_cnt_dict[new_basename] = 1
        new_basename = dt_str + '_' + str(name_cnt_dict[new_basename]) + ext_name
        new_path = os.path.join(dirname, new_basename)
    os.rename(src=img_path_, dst=new_path)
    dst_img_num = dst_img_num + 1
    atime_t = time.mktime(dt.timetuple())
    mtime_t = atime_t
    os.utime(new_path, (atime_t, mtime_t))
    print("Copy new file as :", new_path)


if __name__ == '__main__':
    logger.add("file_{time}.log")
    main_process(base_path)
    print('src img num: ', src_img_num)
    print('dst img num: ', dst_img_num)
