import hashlib
import os
import shutil
from datetime import datetime

from PIL import Image
from loguru import logger

logger.add("{time}.log")


class Sort:
    def __init__(self, src_dir_: str, dst_dir_: str):
        self.__src_dir: str = src_dir_
        self.__dst_dir: str = dst_dir_
        self.__err_dir_root: str = os.path.join(dst_dir_, 'unknown')
        self.__video_dir_root: str = os.path.join(dst_dir_, 'others', 'videos')
        self.__gif_dir_root: str = os.path.join(dst_dir_, 'others', 'gifs')
        self.__sorted_dir_root: str = self.__dst_dir
        self.__src_img_cnt: int = 0
        self.__dst_img_cnt: int = 0
        self.__unknown_img_cnt: int = 0
        self.__name_cnt: dict = {}

    def main_sort(self):
        if self.check_dir_is_valid(self.__src_dir) and self.check_dir_is_valid(self.__dst_dir):
            self.recursive_sort(self.__src_dir)
            logger.info(self.__src_img_cnt)
            logger.info(self.__dst_img_cnt)
        else:
            logger.error('Src or Dst folder is not valid.')

    def recursive_sort(self, path_: str):
        files = os.listdir(path_)
        # todo: update
        for f in files:
            file_path = os.path.join(path_, f)
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

    def sort_img(self, file_: str):
        if self.check_file_type(file_) is 0:
            dt = self.parse_date_exif(file_)
            if dt is not None:
                self.move_exif_img(file_)
            else:
                self.move_unknown_img(file_)
        if self.check_file_type(file_) is 1:
            self.move_unknown_img(file_)
        elif self.check_file_type(file_) in [2, 3]:
            self.move_others(file_)
        else:
            pass
        self.__dst_img_cnt += 1

    @staticmethod
    @logger.catch
    def parse_date_exif(img_file: str):
        """
        extract date info from EXIF data
        :param img_file:
        :return:
        """
        im = Image.open(img_file)
        exif = im.getexif()
        if exif.get(36867) is not None:
            dt_str = exif.get(36867)
            dt = datetime.strptime(dt_str, '%Y:%m:%d %H:%M:%S')
            return dt
        else:
            return None

    @staticmethod
    def check_file_type(src_file_: str):
        """
        todo: more clear method
        0 = jpeg / jpg, 1 = png, 2 = mp4, 3 = gif, None = others
        :rtype: int
        """
        if os.path.basename(src_file_).startswith('.'):
            logger.info(f'{src_file_} is Hidden file, will be skipped')
            return None
        jpg_types = ['.jpeg', '.jpg', '.JPG', '.JPEG']
        png_types = ['.png']
        video_types = ['.mp4']
        gif_types = ['.gif']
        ext = os.path.splitext(src_file_)[1]
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

    def format_file_info(self, file_: str, date_: datetime):
        if date_ is not None:
            # update file date
            atime_t = self.datetime_to_timestamp(date_)
            mtime_t = atime_t
            os.utime(file_, (atime_t, mtime_t))
            # rename file
            dt_str = date_.strftime('%m-%d-%Y (%H%M%S)')
            suffix = self.get_rename_suffix(file_)
            ext = os.path.splitext(file_)[1]
            rename_str = f'{dt_str}{suffix}{ext}'
            dst_file = os.path.join(os.path.dirname(file_), rename_str)
            os.rename(src=file_, dst=dst_file)
        else:
            logger.error('No Date')

    def is_file_duplicate(self, src_file: str, dst_file: str):
        # todo: finish this function
        if os.path.exists(dst_file):
            if self.get_file_md5(src_file) == self.get_file_md5(dst_file):
                logger.warning(f'src file = {src_file} is duplicated, will be skipped')
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def get_file_md5(file_: str):
        buf_size = 65536
        md5 = hashlib.md5()
        with open(file_, 'rb') as f:
            while True:
                data = f.read(buf_size)
                if not data:
                    break
                md5.update(data)
        return md5.hexdigest()

    def move_exif_img(self, src_file: str):
        # create sub dirs
        dt = self.parse_date_exif(src_file)
        year = str(dt.year)
        month = f'{int(dt.month):02}'
        sorted_dir = os.path.join(self.__sorted_dir_root, year, month)

        # copy to dst dir
        self.create_dir(sorted_dir)
        basename = os.path.basename(src_file)
        dst_file = os.path.join(sorted_dir, basename)
        # todo: fix this method
        if self.is_file_duplicate(src_file,
                                  os.path.join(sorted_dir,
                                               dt.strftime('%m-%d-%Y (%H%M%S)') + os.path.splitext(basename)[1])):
            return None
        shutil.copy(src=src_file, dst=dst_file)
        logger.info(f'copy file to = {dst_file}')

        # update file info
        self.format_file_info(file_=dst_file, date_=dt)

    def move_unknown_img(self, src_file: str):
        # no exif info, use mtime instead
        mtime = os.path.getmtime(src_file)
        dt = self.timestamp_to_datetime(mtime)

        # create sub dirs
        divisor = str(self.__unknown_img_cnt // 300)
        unknown_dir = os.path.join(self.__err_dir_root, divisor)
        self.__unknown_img_cnt += 1

        # copy to dst dir
        self.create_dir(unknown_dir)
        basename = os.path.basename(src_file)
        dst_file = os.path.join(unknown_dir, basename)
        # todo: fix this method
        if self.is_file_duplicate(src_file,
                                  os.path.join(unknown_dir,
                                               dt.strftime('%m-%d-%Y (%H%M%S)') + os.path.splitext(basename)[1])):
            return None
        shutil.copy(src=src_file, dst=dst_file)
        logger.info(f'copy file to = {dst_file}')

        # update file info
        self.format_file_info(file_=dst_file, date_=dt)

    def move_others(self, src_file: str):
        if self.check_file_type(src_file) is 2:
            parent_dir = self.__video_dir_root
        elif self.check_file_type(src_file) is 3:
            parent_dir = self.__gif_dir_root
        else:
            return None
        # no exif info, use mtime instead
        dt = self.timestamp_to_datetime(os.path.getmtime(src_file))

        # copy to dst dir
        self.create_dir(parent_dir)
        basename = os.path.basename(src_file)
        dst_file = os.path.join(parent_dir, basename)
        # todo: fix this method
        if self.is_file_duplicate(src_file,
                                  os.path.join(parent_dir,
                                               dt.strftime('%m-%d-%Y (%H%M%S)') + os.path.splitext(basename)[1])):
            return None
        shutil.copy(src=src_file, dst=dst_file)
        logger.info(f'copy file to = {dst_file}')

        # update file info
        self.format_file_info(file_=dst_file, date_=dt)

    @staticmethod
    def create_dir(dir_: str):
        if not os.path.exists(dir_):
            os.makedirs(dir_)
        else:
            pass

    @staticmethod
    def check_dir_is_valid(dir_: str):
        if not os.path.exists(dir_):
            logger.error("No Such Directory = ", dir_)
            return False
        else:
            return True

    @staticmethod
    def timestamp_to_datetime(float_time_):
        return datetime.fromtimestamp(float_time_)

    @staticmethod
    def datetime_to_timestamp(date_: datetime):
        return date_.timestamp()

    def get_rename_suffix(self, name_: str):
        if name_ in self.__name_cnt.keys():
            self.__name_cnt[name_] += 1
            return f'_{self.__name_cnt[name_]}'
        else:
            self.__name_cnt[name_] = 0
            return ''
