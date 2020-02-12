from sort import Sort

if __name__ == '__main__':
    src_dir = '/Volumes/Extreme SSD/Pictures/Sorting/老硬盘备份'
    dst_dir = '/Volumes/Extreme SSD/Pictures/Sorting/老照片整理'
    # src_dir = '/Users/chiya/Pictures/Sorting/Unsort'
    # dst_dir = '/Users/chiya/Pictures/Sorting/Photos_Collection'
    sort = Sort(src_dir_=src_dir, dst_dir_=dst_dir)
    sort.main_sort()
