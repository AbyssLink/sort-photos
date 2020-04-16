from utils import is_file_duplicate, parse_date_exif, is_dir_valid, create_dir
import hashlib
import os
from os import path
import shutil
from datetime import datetime

from PIL import Image
from loguru import logger

logger.add("{time}.log")


class Sort:
    def __init__(self, src_dir: str, dst_dir: str):
        self.__src_dir: str = src_dir
        self.__dst_dir: str = dst_dir
        self.__err_dir_root: str = os.path.join(dst_dir, 'unknown')
        self.__video_dir_root: str = os.path.join(dst_dir, 'others', 'videos')
        self.__gif_dir_root: str = os.path.join(dst_dir, 'others', 'gifs')
        self.__sorted_dir_root: str = self.__dst_dir
        self.__src_img_cnt: int = 0
        self.__dst_img_cnt: int = 0
        self.__unknown_img_cnt: int = 0
        self.__name_cnt: dict = {}

    def main_sort(self):
        if is_dir_valid(self.__src_dir) and is_dir_valid(self.__dst_dir):
            self.recursive_sort(self.__src_dir)
            logger.info(self.__src_img_cnt)
            logger.info(self.__dst_img_cnt)
        else:
            logger.error('Src or Dst folder is not valid.')

    def recursive_sort(self, path: str):
        files = os.listdir(path)
        # todo: update
        for f in files:
            file_path = os.path.join(path, f)
            if os.path.isfile(file_path):
                if self.check_file_type(file_path) is not None:
                    self.__src_img_cnt += 1
                    self.sort_img(file_path)
                else:
                    pass
            elif os.path.isdir(file_path):
                self.recursive_sort(file_path)
            else:
                continue

    def sort_img(self, file: str):
        if self.check_file_type(file) is 0:
            dt = parse_date_exif(file)
            if dt is not None:
                self.move_exif_img(file)
            else:
                self.move_unknown_img(file)
        if self.check_file_type(file) is 1:
            self.move_unknown_img(file)
        elif self.check_file_type(file) in [2, 3]:
            self.move_others(file)
        else:
            pass
        self.__dst_img_cnt += 1

    @staticmethod
    def check_file_type(src_file: str):
        """
        todo: more clear method
        0 = jpeg / jpg, 1 = png, 2 = mp4, 3 = gif, None = others
        :rtype: int
        """
        if os.path.basename(src_file).startswith('.'):
            logger.info(f'{src_file} is Hidden file, will be skipped')
            return None
        jpg_types = ['.jpeg', '.jpg', '.JPG', '.JPEG']
        png_types = ['.png']
        video_types = ['.mp4']
        gif_types = ['.gif']
        ext = os.path.splitext(src_file)[1]
        if ext in jpg_types:
            return 0
        elif ext in png_types:
            return 1
        elif ext in video_types:
            return 2
        elif ext in gif_types:
            return 3
        else:
            return None

    def format_file_info(self, file: str, date: datetime):
        if date is not None:
            # update file date
            atime_t = date.timestamp()
            mtime_t = atime_t
            os.utime(file, (atime_t, mtime_t))
            # rename file
            dt_str = date.strftime('%m-%d-%Y (%H%M%S)')
            suffix = self.get_rename_suffix(file)
            ext = os.path.splitext(file)[1]
            rename_str = f'{dt_str}{suffix}{ext}'
            dst_file = os.path.join(os.path.dirname(file), rename_str)
            os.rename(src=file, dst=dst_file)
        else:
            logger.error('No Date')

    def move_exif_img(self, src_file: str):
        # create sub dirs
        dt = parse_date_exif(src_file)
        year = str(dt.year)
        month = f'{int(dt.month):02}'
        sorted_dir = os.path.join(self.__sorted_dir_root, year, month)

        # copy to dst dir
        create_dir(sorted_dir)
        basename = os.path.basename(src_file)
        dst_file = os.path.join(sorted_dir, basename)
        # todo: fix this method
        if is_file_duplicate(src_file,
                             os.path.join(sorted_dir,
                                          dt.strftime('%m-%d-%Y (%H%M%S)') + os.path.splitext(basename)[1])):
            return None
        shutil.copy(src=src_file, dst=dst_file)
        logger.info(f'copy file to = {dst_file}')

        # update file info
        self.format_file_info(file=dst_file, date=dt)

    def move_unknown_img(self, src_file: str):
        # no exif info, use mtime instead
        mtime = os.path.getmtime(src_file)
        dt = datetime.fromtimestamp(mtime)

        # create sub dirs
        divisor = str(self.__unknown_img_cnt // 300)
        unknown_dir = os.path.join(self.__err_dir_root, divisor)
        self.__unknown_img_cnt += 1

        # copy to dst dir
        create_dir(unknown_dir)
        basename = os.path.basename(src_file)
        dst_file = os.path.join(unknown_dir, basename)
        # todo: fix this method
        if is_file_duplicate(src_file,
                             os.path.join(unknown_dir,
                                          dt.strftime('%m-%d-%Y (%H%M%S)') + os.path.splitext(basename)[1])):
            return None
        shutil.copy(src=src_file, dst=dst_file)
        logger.info(f'copy file to = {dst_file}')

        # update file info
        self.format_file_info(file=dst_file, date=dt)

    def move_others(self, src_file: str):
        if self.check_file_type(src_file) is 2:
            parent_dir = self.__video_dir_root
        elif self.check_file_type(src_file) is 3:
            parent_dir = self.__gif_dir_root
        else:
            return None
        # no exif info, use mtime instead
        dt = datetime.fromtimestamp(os.path.getmtime(src_file))

        # copy to dst dir
        create_dir(parent_dir)
        basename = os.path.basename(src_file)
        dst_file = os.path.join(parent_dir, basename)
        # todo: fix this method
        if is_file_duplicate(src_file,
                             os.path.join(parent_dir,
                                          dt.strftime('%m-%d-%Y (%H%M%S)') + os.path.splitext(basename)[1])):
            return None
        shutil.copy(src=src_file, dst=dst_file)
        logger.info(f'copy file to = {dst_file}')

        # update file info
        self.format_file_info(file=dst_file, date=dt)

    def get_rename_suffix(self, name: str):
        if name in self.__name_cnt.keys():
            self.__name_cnt[name] += 1
            return f'_{self.__name_cnt[name]}'
        else:
            self.__name_cnt[name] = 0
            return ''
