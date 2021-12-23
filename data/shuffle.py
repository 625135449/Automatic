import random
import os
import shutil
from time import sleep
from tqdm import tqdm

def make_test(path,imgpath):
    shuflle_path = path + '/' + 'test'
    if not os.path.exists(shuflle_path):
        os.mkdir(shuflle_path)
    shuflle_imgpath = shuflle_path + '/' + 'images'
    shuflle_lbpath = shuflle_path + '/' + 'labels'
    if not os.path.exists(shuflle_imgpath):
        os.mkdir(shuflle_imgpath)
    if not os.path.exists(shuflle_lbpath):
        os.mkdir(shuflle_lbpath)
    label_path = path + '/' + 'labels'

    for _,_,files in os.walk(imgpath):
        num = int(0.2 * len(files))
        # print(11111)
        result = random.sample(files, num)
        for r in result:
            shutil.copy(os.path.join(imgpath, r), os.path.join(shuflle_imgpath, r))
            # print(2222)

    image_filenames = []      #shuffle pic
    label_names = []          #origin labels
    for _, _, files in os.walk(label_path):
        for f in files:
            if f[-4:] =='.jpg':
                label_names.append(f[:-4])
            # label_names.append(f.split('.')[0])
            else:
                label_names.append(f.split('.')[0])

    for _, _, files in os.walk(shuflle_imgpath):
        for f in files:
            if f[-4:] == '.jpg':
                # label_names.append(f.split('.')[0])
                image_filenames.append(f[:-4])
            else:
                image_filenames.append(f.split('.')[0])
    # print(label_names)
    # print(image_filenames)
    for i in label_names:
        if i in image_filenames:
            remaind_label = i + '.txt'
            shutil.copy(os.path.join(label_path, remaind_label), os.path.join(shuflle_lbpath, remaind_label))
            remove_lb = os.path.join(label_path, i + '.txt')
            remove_img = os.path.join(imgpath, i + '.jpg')
            os.remove(remove_lb)
            os.remove(remove_img)
    print('测试集制作完成')
# make_test('/media/vs/Data/aist/project/glitter0723_2/save', '/media/vs/Data/aist/project/glitter0723_2/save/images')