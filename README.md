# Sort_photos

### Introduction

a simple python script for sorting and organizing photos by date (use exif metadata)

this script will organize unsort photos to different folders by year, month, and rename photo name use photo created timestamp.

### Features

- Organize into folders by time, Read exif DateTimeOriginal (code: 36867) to get time
- Update the photo time and file name, modify the photo's created time to DateTimeOriginal of exif
- Other types of photos (screenshots, png, gif, mp4, etc. without exif information) are categorized into other folders
- Deduplication (determine if the files are the same according to the md5 value of the file)

### Screenshots

![](https://raw.githubusercontent.com/ShiroCheng/pic/master/Sort-photos-Screenshots_1.jpg)



## 中文

### 简介

一个简单的 python 脚本，用于按日期对照片进行排序（使用exif元数据）

此脚本将按年，月将未分类的照片整理到不同的文件夹中，并使用创建的照片时间戳重命名照片名称。

### 功能

- 按时间整理到文件夹，读取 exif DateTimeOriginal (code: 36867) 获得时间
- 更新照片时间和文件名，将照片的 created time 修改为 exif 的 DateTimeOriginal
- 其他类型照片（截图，png, gif, mp4 等无 exif 信息的）归类到其他文件夹
- 去重（依据文件 md5 值判断文件是否相同）

