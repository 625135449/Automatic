import random
import os
import shutil
from tqdm import tqdm


def make_test(path, img_path):
    shuffle_path = f"{path}{'/test'}"
    if not os.path.exists(shuffle_path):
        os.mkdir(shuffle_path)
    shuffle_img_path = f"{shuffle_path}{'/images'}"
    shuffle_lb_path = f"{shuffle_path}{'/labels'}"
    if not os.path.exists(shuffle_img_path):
        os.mkdir(shuffle_img_path)
    if not os.path.exists(shuffle_lb_path):
        os.mkdir(shuffle_lb_path)
    label_path = f"{path}{'/labels'}"

    for _, _, files in os.walk(img_path):
        num = int(0.1 * len(files))
        result = random.sample(files, num)
        for r in result:
            shutil.move(os.path.join(img_path, r), os.path.join(shuffle_img_path, r))

    image_filenames = []  # shuffle pic
    label_names = []  # origin labels
    for _, _, files in os.walk(label_path):
        for f in files:
            label_names.append(f.split('.')[0])

    for _, _, files in os.walk(shuffle_img_path):
        for f in files:
            if f[-4:] == '.jpg':  # 防止有d89ere02fg24.df0r4f.jpg的情况
                image_filenames.append(f[:-4])
            else:
                image_filenames.append(f.split('.')[0])
    for i in tqdm(label_names):  # 全部的label
        if i in image_filenames:  # 转移的图片
            remain_label = f"{i}{'.txt'}"
            shutil.move(os.path.join(label_path, remain_label), os.path.join(shuffle_lb_path, remain_label))
    print('测试集制作完成')

# make_test('/media/vs/Data/aist/project/glitter0723_2/save', '/media/vs/Data/aist/project/glitter0723_2/save/images')
