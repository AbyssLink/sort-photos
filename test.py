import hashlib
import os
from datetime import datetime

import filetype


def main():
    kind = filetype.guess('/Users/chiya/Pictures/Sorting/Unsort/iCloud_Archive/MI 8/Twitter/IMG_20190104_074427.jpg')
    if kind is None:
        print('Cannot guess file type!')
        return

    print('File extension: %s' % kind.extension)
    print('File MIME type: %s' % kind.mime)
    print(type(kind.mime))


def is_file_duplicate(src_file: str, dst_file: str):
    # todo: finish this function
    if os.path.exists(dst_file):
        if get_file_md5(src_file) == get_file_md5(dst_file):
            return True
        else:
            return False
    else:
        return False


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


def test_file_hash():
    print(type(get_file_md5('/Users/chiya/Pictures/Sorting/Photos_Collection/2016/06/06-19-2016 (152730).jpg')))
    print(get_file_md5('/Users/chiya/Pictures/Sorting/Photos_Collection/2016/06/06-19-2016 (152730).jpg'))
    print(get_file_md5('/Users/chiya/Pictures/Sorting/Photos_Collection/2016/06/06-19-2016 (152730)_2.jpg'))


def test():
    img_file = '/Users/chiya/Pictures/MAG/TMP/out.jpg'
    mtime = os.path.getmtime(img_file)
    atime = os.path.getatime(img_file)
    ctime = os.path.getctime(img_file)
    print('mtime = ', time_2_str(mtime))
    print('atime = ', time_2_str(atime))
    print('ctime = ', time_2_str(ctime))
    print(datetime.fromtimestamp(mtime).timestamp())
    print(datetime_to_timestamp(datetime.fromtimestamp(mtime)))
    print(os.path.basename(img_file))
    print(os.path.dirname(img_file))


def time_2_str(time):
    dt = datetime.fromtimestamp(time)
    dt_str = dt.strftime('%m-%d-%Y (%H%M%S)')
    return dt_str


def datetime_to_timestamp(date_: datetime):
    return date_.timestamp()


if __name__ == '__main__':
    test()
    # test_file_hash()
    # test_hidden_file()
