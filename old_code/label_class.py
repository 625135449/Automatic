# coding=utf-8
import sys
import cv2 as cv
import os
from os.path import join
import numpy as np
import time
import screeninfo
import shutil
from PIL import Image, ImageFont, ImageDraw

selected_start = 0
selected_image = 0

label = -1
offset_row = 10
offset_line = 5
line_space = 170
row_space = 173
line_number = 6
row_number = 11
view_w, view_h = 150, 150


def get_mouse(event, x, y, flags, param):
    global selected_image, label, page, selected_start
    if event == 1:
        if flags == 1:
            line_index = int((y - offset_line) / line_space)
            row_index = int((x - offset_row) / row_space)
            selected_image = line_index * row_number + row_index + page * row_number * line_number
            label = -1
            display()
        if flags == 9:
            line_index = int((y - offset_line) / line_space)
            row_index = int((x - offset_row) / row_space)
            selected_start = line_index * row_number + row_index + page * row_number * line_number
            label = -1
            display()


fconf = open('conf.txt', 'r')
classes = dict()
for lll in fconf.readlines():
    ls = lll.replace('\r', '').replace('\n', '').split(',')
    classes[ls[0]] = [ls[1], ls[2]]
fconf.close()

# fconf = open('dir.txt', 'r')
# target_dir_root = fconf.readlines()[0].replace('\r', '').replace('\n', '')
target_dir_root = sys.argv[1]
target_dir = target_dir_root
fconf.close()

image_buffer_list = [None for j in range(line_number * row_number)]

cv.namedWindow('PPG', cv.WINDOW_GUI_NORMAL)
#cv.namedWindow('PPG', cv.WINDOW_GUI_NORMAL)
cv.moveWindow('PPG', -1, -1)
#cv.setWindowProperty('PPG', cv.WND_PROP_AUTOSIZE, cv.WINDOW_AUTOSIZE)
cv.setWindowProperty('PPG', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
cv.setMouseCallback('PPG', get_mouse)

is_exit = 0
image_loaded = False
image_number = 0
image_list_len = 0
page = 0
check_title = '未标注'


def change_class():
    global target_dir, classes, check_title, selected_start
    info = ''
    keys = list(classes.keys())
    keys.sort()
    c = map(classes.get, keys)
    for ci, values in enumerate(c):

        info = '%s %d - %s ' % (info, ci, values[0])
    info = '%s %s - %s ' % (info, 'a', '未标注')
    display('[请选择需要检查的分类]', info, (0, 255, 50), (255, 255, 255))
    key = cv.waitKey(0) & 0xff
    if ord('0') <= key <= ord('9'):
        if chr(key) in classes.keys():
            target_dir = join(target_dir_root, classes[chr(key)][1])
            check_title = classes[chr(key)][0]
            selected_start = 0

    if key in [ord('a')]:
        target_dir = target_dir_root
        check_title = '未标注'
        selected_start = 0


def YesOrNo(title, msg, color1=(200, 200, 200), color2=(255, 255, 255)):
    display(title, msg, color1, color2)
    key = cv.waitKey(0) & 0xff
    if key == ord('y'):
        return True
    else:
        return False


def print_info(frame, st1, st, color1, color2):
    img = Image.fromarray(frame)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('deng.ttf', 22)
    draw.text(xy=(10, 1055), text=st, font=font, fill=color1)
    draw.text(xy=(10, 1030), text=st1, font=font, fill=color2)
    draw.text(xy=(10, 0), text=sys.argv[1] + '  (' + sys.argv[2] + ')', font=font, fill=(0, 0, 0))

    frame = np.asanyarray(img)
    return frame


def load_image(fn):
    global image_buffer_list
    imt = cv.imread(join(target_dir, fn[0]))
    image_buffer_list[fn[1]] = cv.resize(imt, (view_w, view_h))


def display(other_info1=None, other_info2=None, color1=(200,200,200), color2=(255,255,255)):
    global image_buffer_list, offset_line, offset_row, label, selected_start, selected_image, image_number, image_list_len, page, classes
    im_dis = np.zeros([1080, 1920, 3], dtype=np.uint8)
    info = ''
    info1 = ''
    for i in range(image_number):
        line = int(i / row_number)
        row = i % row_number
        im_dis[offset_line + line * line_space: offset_line + line * line_space + view_h, offset_row + row * row_space: offset_row + row * row_space + view_w, :] = image_buffer_list[i]
        if selected_start < page * row_number * line_number + i < selected_image:
            cv.rectangle(im_dis, (offset_row + row * row_space - 5, offset_line + line * line_space - 5),
                         (offset_row + row * row_space + view_w + 4, offset_line + line * line_space + view_h + 4), thickness=2,
                         color=(150, 150, 255))

    if image_list_len % (line_number * row_number) == 0:
        total_page = int(image_list_len / (line_number * row_number))
    else:
        total_page = int(image_list_len / (line_number * row_number)) + 1

    if len(image_list) > 0:
        info1 = '[%s] 页面：%d/%d (剩余: %d)  [操作: x 退出 <> 翻页 c 检查]  |  开始图片: %d (%s)' % (check_title, page + 1,  total_page , image_list_len, selected_start, image_list[selected_start])

    if selected_start > selected_image:
        selected_t = selected_start
        selected_start = selected_image
        selected_image = selected_t

    local_start = -1
    local_end = -1

    if selected_image >= 0 and image_list_len > 0:
        info1 = '%s 结束图片: %d (%s)' % (info1, selected_image, image_list[selected_image])
        located_page = int(selected_image / (line_number * row_number))
        if located_page < page:
            local_start = 0

        if located_page == page:
            info = '分类选择: '
            si = selected_image % (line_number * row_number)
            line = int(si / row_number)
            row = si % row_number
            cv.rectangle(im_dis, (offset_row + row * row_space - 5, offset_line + line * line_space - 5),
                         (offset_row + row * row_space + view_w + 4, offset_line + line * line_space + view_h + 4),
                         thickness=2,
                         color=(255, 255, 255))
            keys = list(classes.keys())
            keys.sort()
            c = map(classes.get, keys)
            for ci, values in enumerate(c):
                    info = '%s %d - %s ' % (info, ci, values[0])

    if selected_start >= 0:
        located_page = int(selected_start / (line_number * row_number))
        if located_page == page:
            si = selected_start % (line_number * row_number)
            line = int(si / row_number)
            row = si % row_number
            cv.rectangle(im_dis, (offset_row + row * row_space - 5, offset_line + line * line_space - 5),
                         (offset_row + row * row_space + view_w + 4, offset_line + line * line_space + view_h + 4),
                         thickness=2,
                         color=(0, 0, 255))

    if label >= 0:
        info = '%s   [已选择 %d: %s]   按 [ENTER] 确定分类' % (info, label, classes['%d' % label][0])
    if other_info1 is None:
        other_info1 = info1
    if other_info2 is None:
        other_info2 = info
    im_dis = print_info(im_dis, other_info1, other_info2, color1, color2)

    cv.imshow('PPG', im_dis)


if __name__ == '__main__':
    diff_list = {}

    with open(join(target_dir, 'diff.txt'), 'r') as fid:
        diffs = fid.readlines()

    for d in diffs:
        d = d.strip()
        k = d.split(',')[0]
        v = float(d.split(',')[1])
        diff_list[k] = v

    while True:
        label = -1
        selected_start = 0
        selected_image = 0

        if os.path.exists(target_dir):
            t_list = os.listdir(target_dir)
        else:
            os.mkdir(target_dir)
            t_list = os.listdir(target_dir)
        t_list.sort()
        image_list = list()
        image_loaded = False
        for l in t_list:
            if l[-3:] == 'jpg':
                image_list.append(l)

        image_list_len = len(image_list)
        for img_i, img in enumerate(image_list):
            if img in diff_list.keys() and img_i > 0:
                if diff_list[img] > 0.06:
                    selected_image = img_i - 1
                    break
                else:
                    selected_image = img_i

        page = int(selected_image / (line_number * row_number))

        while True:
            image_number = line_number * row_number

            if (page + 1) * (line_number * row_number) > image_list_len:
                image_number = image_list_len - page * (line_number * row_number)

            image_name_list = image_list[page * (line_number * row_number): page * (line_number * row_number) + image_number]
            image_list_for_load = []
            for i in range(image_number):
                image_list_for_load.append([image_name_list[i], i])

            if image_loaded is False:
                for ilfl in image_list_for_load:
                    load_image(ilfl)
                image_loaded = True

            if image_list_len == 0:
                display('[恭喜]', '标注完成, 请按 c 键检查.', (255, 64, 0), (255, 64, 0))
            else:
                display()

            key = cv.waitKey(0) & 0xff

            if key in [39]:
                if (page + 10) * line_number * row_number < image_list_len or \
                        ((page + 10) * line_number * row_number == image_list_len and
                         image_list_len % (line_number * row_number) > 0):
                    page = page + 10
                    image_loaded = False
                    label = -1

            if key in [59]:
                if page > 10:
                    page = page - 10
                    image_loaded = False
                    label = -1


            if key in [46]:

                if (page + 1) * line_number * row_number < image_list_len or \
                        ((page + 1) * line_number * row_number == image_list_len and
                         image_list_len % (line_number * row_number) > 0):
                    page = page + 1
                    image_loaded = False
                    label = -1

            if key in [44]:
                if page > 0:
                    page = page - 1
                    image_loaded = False
                    label = -1

            if key in [ord('x')]:
                if YesOrNo('[注意]', '确定退出请按 Y 键, 按其他键取消。', (0,255,255), (0,255,255)):
                    is_exit = 1
                    break

            if key in [27]:
                if YesOrNo('[注意]', '确定退出请按 Y 键, 按其他键取消。', (0,255,255), (0,255,255)):
                    is_exit = 2
                    break

            if selected_image >= 0:
                if ord('0') <= key <= ord('9'):
                    if '%d' % (key - ord('0')) in classes.keys():
                        label = key - ord('0')

            if key in [13]:
                if selected_image >= 0:
                    if label >= 0:
                        for copy_index in range(selected_start, selected_image + 1):
                            if os.path.exists(join(target_dir, classes['%d' % label][1])) is False:
                                os.mkdir(join(target_dir, classes['%d' % label][1]))
                            shutil.move(join(target_dir, image_list[copy_index]), join(target_dir_root, classes['%d' % label][1],
                                                                                       image_list[copy_index]))
                        break

            if key in [ord('c')]:
                change_class()
                break

        if is_exit == 1:
            sys.exit(0)

        if is_exit == 2:
            sys.exit(1)
