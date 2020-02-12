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


def test():
    img_file = '/Users/chiya/Pictures/Sorting/Unsort/老照片/来自：GT-I9500(1)/Screenshots/Screenshot_2016-07-19-12-57-09.png'
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
