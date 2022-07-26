import os
import cv2 as cv
from os.path import join, exists, splitext
import json_report
from pprint import pprint
import numpy as np
from multiprocessing.pool import Pool
from multiprocessing import cpu_count
import time


def have_dir(p):
    if exists(p) is False:
        os.mkdir(p)


def no_file(p):
    if exists(p):
        os.remove(p)


def get_diff(folder):
    no_file(join(folder, 'diff.txt'))

    file_list = os.listdir(folder)

    file_list.sort()

    f_pre = None

    for img_i, img_file in enumerate(file_list):
        if splitext(img_file)[1].lower() in ['.jpg']:
            f = cv.imread(join(folder, img_file))
            if img_i > 0:
                diff = sum(sum(sum(np.abs(f.astype(np.int64) - f_pre.astype(np.int64))))) / float(256 * 256 * 3 * 256)
                with open(join(folder, 'diff.txt'), 'a') as fid:
                    fid.write('%s,%7.6f\n' % (img_file, diff))
                    print(folder, img_file, '%7.6f' % diff)
            f_pre = f.copy()


def get_aist_sub_folder(unlabelled_root_dir):
    unlabelled_dir_list = os.listdir(unlabelled_root_dir)

    process_list = []

    for unlabelled_dir in unlabelled_dir_list:
        if os.path.isdir(join(unlabelled_root_dir, unlabelled_dir)):
            sub_unlabelled_dir_list = os.listdir(join(unlabelled_root_dir, unlabelled_dir))
            for sub_unlabelled_dir in sub_unlabelled_dir_list:
                if os.path.isdir(join(unlabelled_root_dir, unlabelled_dir, sub_unlabelled_dir)):
                    video_dir_list = os.listdir(join(unlabelled_root_dir, unlabelled_dir, sub_unlabelled_dir))
                    for video_dir in video_dir_list:
                        if os.path.isdir(join(unlabelled_root_dir, unlabelled_dir, sub_unlabelled_dir, video_dir)):
                            pos_dir_list = os.listdir(join(unlabelled_root_dir, unlabelled_dir, sub_unlabelled_dir, video_dir))
                            for pos_dir in pos_dir_list:
                                process_list.append(join(unlabelled_root_dir, unlabelled_dir, sub_unlabelled_dir, video_dir, pos_dir))
    return process_list


def aist_diff(pl):

    pool = Pool(cpu_count() - 1)
    pl.sort()
    pool.map(get_diff, pl)


if __name__ == '__main__':
    process_list = get_aist_sub_folder('/home/amax/code/ppg_pulling_unlabelled')

    for i, pl in enumerate(process_list):
        if os.system('python3 label_class.py "%s" "%d/%d"' % (pl, i, len(process_list))) != 0:
            break
    #aist_diff(process_list)

