from sort import Sort

if __name__ == '__main__':
    src_dir = input('Source directory: ')
    dst_dir = input('Destination directory: ')
    sort = Sort(src_dir=src_dir, dst_dir=dst_dir)
    sort.main_sort()
