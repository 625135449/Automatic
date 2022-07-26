import os
import cv2 as cv
from os.path import join, exists, splitext
import json_report
from pprint import pprint
import numpy as np
from multiprocessing.pool import Pool
from multiprocessing import cpu_count
import time


def prefix_match(value, p):
    value = os.path.split(value)[-1]
    for k in p.keys():
        if value[:len(k)] == k:
            return True, k
    return False, None


def have_dir(p):
    if exists(p) is False:
        os.mkdir(p)


def no_file(p):
    if exists(p):
        os.remove(p)


def process_one_video(p):
    video_file = p[0]
    video_file_root = os.path.splitext(os.path.split(video_file)[-1])[0]
    seg = p[1]
    sub_unlabelled_dir = p[3]

    regions = seg['regions']
    seg_name = seg['name']

    have_dir(join(sub_unlabelled_dir, seg_name))
    have_dir(join(sub_unlabelled_dir, seg_name, video_file_root))

    cw = join(sub_unlabelled_dir, seg_name, video_file_root)

    for reg in regions:
        have_dir(join(cw, reg['name']))
        no_file(join(cw, reg['name'], 'diff.txt'))

    cap = cv.VideoCapture(video_file)

    f_pre = None
    t = time.time()
    ttf = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    for i in range(ttf):
        cap.grab()

        if i % 300 != 0:
            continue
        _, f = cap.retrieve()

        dt = time.time() - t
        print(video_file_root, int(cap.get(cv.CAP_PROP_FRAME_COUNT)), i, dt, int((ttf - i) / 300 * dt / 60))
        t = time.time()
        if f is not None:
            for reg in regions:
                sub_img = f[reg['y']:reg['y'] + reg['h'], reg['x']:reg['x'] + reg['w'], :]
                cv.imwrite(join(cw, reg['name'], '%08d.jpg' % i), sub_img)
                if i != 0:
                    with open(join(cw, reg['name'], 'diff.txt'), 'a') as fid:
                        diff = sum(sum(sum(np.abs(f.astype(np.uint32) - f_pre.astype(np.uint32)))))
                        fid.write('%08d.jpg,%d\n' % (i, diff))
                        print(video_file_root, int(cap.get(cv.CAP_PROP_FRAME_COUNT)), i, '%6.3f' % dt,
                              int((ttf - i) / 300 * dt / 60), diff)

            f_pre = f.copy()


def process_raw_dir(sub_raw_dir, sub_unlabelled_dir):
    if exists(sub_raw_dir) is False:
        os.mkdir(sub_raw_dir)
    if exists(sub_unlabelled_dir) is False:
        os.mkdir(sub_unlabelled_dir)

    raw_file_list = os.listdir(sub_raw_dir)
    seg_file_list = []
    video_file_list = []

    for f in raw_file_list:
        if splitext(f)[1].lower() in ['.mp4']:
            video_file_list.append(join(sub_raw_dir, f))
        if splitext(f)[1].lower() in ['.seg']:
            seg_file_list.append(join(sub_raw_dir, f))

    seg_info = {}
    for seg_file in seg_file_list:
        with open(seg_file, 'r') as fid:
            seg_dict = json_report.load(fid)
            seg_info.update(seg_dict)

    process_list = []
    for video_file in video_file_list:
        pm = prefix_match(video_file, seg_info)
        if pm[0]:
            process_list.append([video_file, seg_info[pm[1]], sub_raw_dir, sub_unlabelled_dir])

    pool = Pool(cpu_count() - 1)
    pool_len = cpu_count() - 1

    pool.map(process_one_video, process_list)


def aist_pp_classification(raw_root_dir, unlabelled_root_dir):
    raw_dir_list = os.listdir(raw_root_dir)
    for raw_dir in raw_dir_list:
        if os.path.isdir(join(raw_root_dir, raw_dir)):
            process_raw_dir(join(raw_root_dir, raw_dir), join(unlabelled_root_dir, raw_dir))


if __name__ == '__main__':
    aist_pp_classification('/data/ppg/raw', '/home/amax/code/unlabelled')