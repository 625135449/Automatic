import os
from os.path import join, splitext, exists
import cv2 as cv
from models import *
import json_report
from tqdm import tqdm
from multiprocessing.pool import Pool
from multiprocessing import cpu_count
import multiprocessing as mp
import random
import time
img_bg = None
#cwd = os.getcwd()
#cwd = '/home/vs/code/aist'
cwd = '/media/vs/Data/aist'


def input_window(img, msg, color='blue'):
    print(msg)
    return input('>')


def create_new_classification_project(project_name):
    os.mkdir(join('.', 'project', project_name))
    os.mkdir(join('.', 'project', project_name, 'data'))
    os.mkdir(join('.', 'project', project_name, 'data', 'train'))
    os.mkdir(join('.', 'project', project_name, 'model'))
    os.mkdir(join('.', 'project', project_name, 'weight'))

    classes = input_window(img_bg, 'Input names of classes \n(separated by ",", no space, eg: apple,orange):').strip()
    class_list = classes.split(',')
    class_number = len(class_list)

    net_type = input_window(img_bg, 'D9, D19?')

    model_cfg = ''

    if net_type.lower() == 'd9':
        model_cfg = class_d9

    # Make "data" and "name" file

    data_file = '''classes= %d
train  = %s
valid  = %s
names = %s
backup = %s
labels = %s
    ''' % (
        class_number, join(cwd, 'project', project_name, 'model', 'train.txt'),
        join(cwd, 'project', project_name, 'model', 'test.txt'),
        join(cwd, 'project', project_name, 'model', 'name.txt'),
        join(cwd, 'project', project_name, 'weight'),
        join(cwd, 'project', project_name, 'model', 'name.txt')
    )
    with open(join(cwd, 'project', project_name, 'model', 'data.txt'), 'w') as fid:
        fid.write(data_file)

    with open(join(cwd, 'project', project_name, 'model', 'name.txt'), 'w') as fid:
        for class_name in class_list:
            fid.write('%s\n' % class_name)

    # Settings
    settings = {'CLASS_NUMBER': class_number,
                'FILTER_NUMBER': class_number,
                'LEARNING_RATE': 0.01,
                'MAX_STEP_100': 10000,
                'MAX_STEP_80': 8000,
                'MAX_STEP_90': 9000,
                'VERSION': net_type,
                'CLASSES': classes
                }

    # Make network
    for k in settings.keys():
        if isinstance(settings[k], str) is False:
            model_cfg = model_cfg.replace('{' + k + '}', '{:g}'.format(settings[k]))
        else:
            model_cfg = model_cfg.replace('{' + k + '}', settings[k])

    with open(join(cwd, 'project', project_name, 'model', project_name + '.cfg'), 'w') as fid:
        fid.write('%s' % model_cfg)

    with open(join(cwd, 'project', project_name, 'settings.json_report'), 'w') as fid:
        json_report.dump(settings, fid)

    print('Project "%s" is created. \nPlease move the labelled images to project/%s/data/train/ and run this APP again to train.' % (
        project_name, project_name))
    print('Example:\n...data/train/class1/images.jpg')
    print('...data/train/class2/images.jpg')
    print('Images should be in .jpg format.')


def create_new_detection_project(project_name):
    os.mkdir(join('.', 'project', project_name))
    os.mkdir(join('.', 'project', project_name, 'data'))
    os.mkdir(join('.', 'project', project_name, 'data', 'raw'))
    os.mkdir(join('.', 'project', project_name, 'data', 'train'))
    os.mkdir(join('.', 'project', project_name, 'data', 'train', 'images'))
    os.mkdir(join('.', 'project', project_name, 'data', 'train', 'labels'))
    os.mkdir(join('.', 'project', project_name, 'data', 'train', 'masks'))
    os.mkdir(join('.', 'project', project_name, 'data', 'view'))
    os.mkdir(join('.', 'project', project_name, 'model'))
    os.mkdir(join('.', 'project', project_name, 'weight'))

    classes = input_window(img_bg, 'Input names of classes \n(separated by ",", no space, eg: apple,orange):').strip()
    class_list = classes.split(',')
    class_number = len(class_list)

    net_type = input_window(img_bg, 'V4, V3T, V4T?')

    model_cfg = ''

    if net_type.lower() == 'v4':
        # CLASS_NUMBER,  FILTER_NUMBER, LEARNING_RATE,  MAX_STEP
        model_cfg = yolo_v4

    if net_type.lower() == 'v3t':
        # CLASS_NUMBER,  FILTER_NUMBER, LEARNING_RATE,  MAX_STEP
        model_cfg = yolo_v3_tiny

    if net_type.lower() == 'v4t':
        # CLASS_NUMBER,  FILTER_NUMBER, LEARNING_RATE,  MAX_STEP
        model_cfg = yolo_v4_tiny

    # Make "data" and "name" file

    data_file = '''classes= %d
train  = %s
valid  = %s
names = %s
backup = %s''' % (class_number, join(cwd, 'project', project_name, 'model', 'train.txt'),
        join(cwd, 'project', project_name, 'model', 'test.txt'),
        join(cwd, 'project', project_name, 'model', 'name.txt'), join(cwd, 'project', project_name, 'weight'))
    with open(join(cwd, 'project', project_name, 'model', 'data.txt'), 'w') as fid:
        fid.write(data_file)

    with open(join(cwd, 'project', project_name, 'model', 'name.txt'), 'w') as fid:
        for class_name in class_list:
            fid.write('%s\n' % class_name)

    # Settings
    settings = {'CLASS_NUMBER': class_number,
                'FILTER_NUMBER': (class_number + 5) * 3,
                'LEARNING_RATE': 0.00261 / 4,
                'MAX_STEP_100': 10000,
                'MAX_STEP_80': 8000,
                'MAX_STEP_90': 9000,
                'VERSION': net_type,
                'CLASSES': classes
                }

    # Make network
    for k in settings.keys():
        if isinstance(settings[k], str) is False:
            model_cfg = model_cfg.replace('{' + k + '}', '{:g}'.format(settings[k]))
        else:
            model_cfg = model_cfg.replace('{' + k + '}', settings[k])

    with open(join(cwd, 'project', project_name, 'model', project_name + '.cfg'), 'w') as fid:
        fid.write('%s' % model_cfg)

    with open(join(cwd, 'project', project_name, 'settings.json_report'), 'w') as fid:
        json_report.dump(settings, fid)

    print('Project "%s" is created. \nPlease move the raw training folder including "image" and "mask" folders to project/%s/data/raw/ and run this APP again to train.' % (
        project_name, project_name))
    print('Example:\n...raw/data_20200101/mask')
    print('...raw/data_20200101/image')
    print('Images should be in .jpg format, while mask should be in .png format.')


def create_new_project(project_name):
    dcs = input_window(img_bg, 'Detection or classification?').strip().lower()
    if dcs in ['detection', 'd']:
        create_new_detection_project(project_name)
    elif dcs in ['classficication', 'c']:
        create_new_classification_project(project_name)


def check_project(project_name):
    project_dir = join('project', project_name)
    print('Model settings:')
    with open(join(project_dir, 'settings.json_report'), 'r') as fid:
        settings = json_report.load(fid)
    for k in settings.keys():
        print('    %s: %s' % (k, settings[k]))

    if settings['VERSION'].lower() in ['v3t', 'v3', 'v4', 'v4t']:
        return check_detection_project(project_name, settings)

    if settings['VERSION'].lower() in ['d9', 'd19']:
        return check_classification_project(project_name, settings)


def find_all_image(folder, image_class):

    file_list = os.listdir(folder)
    file_list.sort()

    for f in file_list:
        if os.path.isdir(join(folder, f)):
            find_all_image(join(folder, f), image_class)
        else:
            for k in image_class.keys():
                if k in join(folder, f):
                    image_class[k].append(join(folder, f))


def check_classification_project(project_name, settings):
    project_dir = join('project', project_name)
    print('Training state:')

    weight_list = os.listdir(join(project_dir, 'weight'))
    weight_list.sort()
    num = [0]
    for w in weight_list:
        if project_name in w:
            try:
                num.append(int(w.split('_')[-1].split('.')[0]))
            except:
                pass

    total = max(num)
    print('    Weight files number: %d' % len(weight_list))
    print('    Max training epoch: %d' % total)

    class_name = settings['CLASSES'].split(',')

    image_class = {}

    print('Data:')

    for cn in class_name:
        image_class[cn] = []

    find_all_image(join(project_dir, 'data', 'train'), image_class)

    total_number = 0
    for k in class_name:
        total_number += len(image_class[k])
        print('    %s: %d' % (k, len(image_class[k])))

    print('    (Total: %d)' % total_number)
    return image_class, settings, total


def check_detection_project(project_name, settings):
    project_dir = join('project', project_name)

    print('Training state:')
    weight_list = os.listdir(join(project_dir, 'weight'))
    weight_list.sort()
    num = [0]
    for w in weight_list:
        if project_name in w:
            try:
                num.append(int(w.split('_')[-1].split('.')[0]))
            except:
                pass

    total = max(num)
    print('    Weight files number: %d' % len(weight_list))
    print('    Max training epoch: %d' % total)

    print('Raw Data:')
    raw_dir_list = os.listdir(join(project_dir, 'data', 'raw'))
    raw_dir_list.sort()
    print('   RAW Folders: %s' % ', '.join(raw_dir_list))
    ava_image_list = []
    total_number = 0
    for rd in raw_dir_list:
        if os.path.isdir(join(project_dir, 'data', 'raw', rd)) is False:
            continue
        ava_image_list_dir = []
        images_list = os.listdir(join(project_dir, 'data', 'raw', rd, 'image'))
        masks_list = os.listdir(join(project_dir, 'data', 'raw', rd, 'mask'))
        for imf in images_list:
            if os.path.splitext(imf)[1].lower() in ['.jpg', '.bmp', '.png', '.jpeg']:
                if os.path.exists(join(project_dir, 'data', 'raw', rd, 'mask', 'mask ' + os.path.splitext(imf)[0] + '.png')):
                    ava_image_list_dir.append([join(project_dir, 'data', 'raw', rd, 'image', imf),
                                               join(project_dir, 'data', 'raw', rd, 'mask',
                                                    'mask ' + os.path.splitext(imf)[0] + '.png')])
                    if os.path.exists(join(project_dir, 'data', 'raw', rd, 'label', os.path.splitext(imf)[0] + '.txt')):
                        ava_image_list_dir[-1].append(join(project_dir, 'data', 'raw', rd, 'label', os.path.splitext(imf)[0] + '.txt'))
                else:
                    print(imf)
            else:
                print(imf)

        print('    %s: image(%d), mask(%d), matched(%d)' % (rd, len(images_list), len(masks_list), len(ava_image_list_dir)))
        ava_image_list.append(ava_image_list_dir)
        total_number += len(ava_image_list_dir)

    print('    Total: %d' % total_number)
    print('Training Data:')
    if os.path.exists(join(project_dir, 'data', 'train', 'images')) and os.path.exists(join(project_dir, 'data', 'train', 'labels')):
        train_images = os.listdir(join(project_dir, 'data', 'train', 'images'))
        train_labels = os.listdir(join(project_dir, 'data', 'train', 'labels'))
        train_images_matched = []
        for ti in train_images:
            if os.path.splitext(ti)[0] + '.txt' in train_labels:
                train_images_matched.append(ti)
        print('    Images(%d) Labels(%d) Matched(%d)' % (len(train_images), len(train_labels), len(train_images_matched)))
    else:
        print('    No training data are created.')

    return ava_image_list, settings, total


def more_data(sample):
    project_dir = sample[-1]
    img_path = sample[0]
    mask_path = sample[1]
    #print(len(sample))
    if len(sample) == 5:
        r = sample[4]
    else:
        r = 1.1
    img = cv.imread(img_path)
    mask = cv.imread(mask_path)
    img_file = os.path.split(img_path)[1]
    img_h, im_w = img.shape[:2]

    cv.imwrite(join(project_dir, 'data', 'train', 'images', os.path.splitext(img_file)[0] + '.jpg'), img)
    img_fh = cv.flip(img, 1)
    cv.imwrite(join(project_dir, 'data', 'train', 'images', os.path.splitext(img_file)[0] + '+fh.jpg'), img_fh)
    # img_fv = cv.flip(img, 0)
    # cv.imwrite(join(project_dir, 'data', 'train', 'images', os.path.splitext(img_file)[0] + '+fv.jpg'), img_fv)
    # img_fvh = cv.flip(img_fv, 1)
    # cv.imwrite(join(project_dir, 'data', 'train', 'images', os.path.splitext(img_file)[0] + '+fvh.jpg'), img_fvh)


    def larger_bbox(xt, yt, wt, ht, r):
        if r == 1:
            return xt, yt, wt, ht
        wt = wt * r
        ht = ht * r
        if xt - wt // 2 < 0:
            wt = xt * 1.99
        if xt + wt // 2 > 1:
            wt = (1 - xt) * 1.99

        if yt - ht // 2 < 0:
            ht = yt * 1.99
        if yt + ht // 2 > 1:
            ht = (1 - yt) * 1.99

        return xt, yt, wt, ht
    # label
    if len(sample) >= 4:
        with open(sample[2], 'r') as fid:
            label_lines = fid.readlines()
        labels = []
        for l in label_lines:
            ls = l.strip().split(' ')
            labels.append([int(ls[0]), float(ls[1]), float(ls[2]), float(ls[3]), float(ls[4])])

        with open(join(project_dir, 'data', 'train', 'labels', os.path.splitext(img_file)[0] + '.txt'), 'w') as fid:
            for l in labels:
                cat, x, y, w, h = l
                x, y, w, h = larger_bbox(x, y, w, h, r)
                fid.write('%d %7.6f %7.6f %7.6f %7.6f\n' % (cat, x, y, w, h))
        with open(join(project_dir, 'data', 'train', 'labels', os.path.splitext(img_file)[0] + '+fh.txt'), 'w') as fid:
            for l in labels:
                cat, x, y, w, h = l
                x, y, w, h = larger_bbox(x, y, w, h, r)
                fid.write('%d %7.6f %7.6f %7.6f %7.6f\n' % (cat, 1-x, y, w, h))
        # with open(join(project_dir, 'data', 'train', 'labels', os.path.splitext(img_file)[0] + '+fv.txt'), 'w') as fid:
        #     for l in labels:
        #         cat, x, y, w, h = l
        #         fid.write('%d %7.6f %7.6f %7.6f %7.6f\n' % (cat, x, 1-y, w, h))
        # with open(join(project_dir, 'data', 'train', 'labels', os.path.splitext(img_file)[0] + '+fvh.txt'), 'w') as fid:
        #     for l in labels:
        #         cat, x, y, w, h = l
        #         fid.write('%d %7.6f %7.6f %7.6f %7.6f\n' % (cat, 1-x, 1-y, w, h))

    # mask
    cv.imwrite(join(project_dir, 'data', 'train', 'masks', os.path.splitext(img_file)[0] + '.png'), mask)
    cv.imwrite(mask_path, mask)
    mask_fh = cv.flip(mask, 1)
    cv.imwrite(join(project_dir, 'data', 'train', 'masks', os.path.splitext(img_file)[0] + '+fh.png'), mask_fh)
    # mask_fv = cv.flip(mask, 0)
    # cv.imwrite(join(project_dir, 'data', 'train', 'masks', os.path.splitext(img_file)[0] + '+fv.png'), mask_fv)
    # mask_fvh = cv.flip(mask_fv, 1)
    # cv.imwrite(join(project_dir, 'data', 'train', 'masks', os.path.splitext(img_file)[0] + '+fvh.png'), mask_fvh)


def make_data(project_name, sample_list):
    project_dir = join('project', project_name)
    os.system('rm %s/*' % join(project_dir, 'data', 'train', 'images'))
    os.system('rm %s/*' % join(project_dir, 'data', 'train', 'labels'))
    os.system('rm %s/*' % join(project_dir, 'data', 'train', 'masks'))
    os.system('rm %s/*' % join(project_dir, 'data', 'view'))

    # More data
    pool = Pool(cpu_count() - 1)
    pool_len = cpu_count() - 1
    #r = pool.map(pcs_img, file_list)

    sample_pool = []
    for sample in tqdm(sample_list):
        sample.append(project_dir)
        sample_pool.append(sample)
        if len(sample_pool) >= pool_len:
            r = pool.map(more_data, sample_pool)
            sample_pool = []
    if sample_pool is not []:
        r = pool.map(more_data, sample_pool)


def mask_to_label_pcs(para):
    class_color = [[128, 0, 0], [0, 128, 0]]

    f = para[0]
    project_dir = para[1]
    name_root = os.path.splitext(f)[0].replace('mask ', '')

    if os.path.splitext(f)[1].lower() not in ['.png']:
        return
    im = cv.imread(join(project_dir, 'data', 'train', 'masks', name_root + '.png'))
    imc = cv.imread(join(project_dir, 'data', 'train', 'images', name_root + '.jpg'))

    if exists(join(project_dir, 'data', 'train', 'labels', name_root + '.txt')) is False:
        fid = open(join(project_dir, 'data', 'train', 'labels', name_root + '.txt'), 'w')

        h, w = im.shape[:2]
        imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(imgray, 10, 255, 0)
        contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            leftmost = tuple(cnt[cnt[:, :, 0].argmin()][0])[0]
            rightmost = tuple(cnt[cnt[:, :, 0].argmax()][0])[0]
            topmost = tuple(cnt[cnt[:, :, 1].argmin()][0])[1]
            bottommost = tuple(cnt[cnt[:, :, 1].argmax()][0])[1]

            rect = [[(leftmost + rightmost) / 2, (topmost + bottommost) / 2], [rightmost - leftmost, bottommost - topmost]]
            center_x, center_y = int(rect[0][0]), int(rect[0][1])
            b, g, r = im[center_y, center_x, :]
            class_index = -1
            for cc_i, cc in enumerate(class_color):
                if cc == [r, g, b]:
                    class_index = cc_i
                    break

            # Special cases
            if class_index == 1 and 'r3_b' in f:
                rect[1][0] *= 0.8
                rect[1][1] *= 0.8

            imc = cv.rectangle(imc, (int(rect[0][0]) - int(rect[1][0] / 2), int(rect[0][1]) - int(rect[1][1] / 2)),
                              (int(rect[0][0]) + int(rect[1][0] / 2), int(rect[0][1]) + int(rect[1][1] / 2)),
                               (0, 255, 0), thickness=1)
            fid.write('%d %7.6f %7.6f %7.6f %7.6f\n' % (0, rect[0][0] / w, rect[0][1] / h, rect[1][0] / w, rect[1][1] / h))
        fid.close()

        try:
            if 1:#len(f.split('+')) == 1:  # 被改过的
                cv.imwrite(join(project_dir, 'data', 'view', name_root + '.jpg'), imc)
        except:
            print('Bug', name_root)
    else:
        with open(join(project_dir, 'data', 'train', 'labels', name_root + '.txt'), 'r') as fid:
            labels = fid.readlines()
            h, w = imc.shape[:2]
            for label in labels:
                cc, xr, yr, wr, hr = label.strip().split(' ')
                xr, yr, wr, hr = int(float(xr) * w), int(float(yr) * h), int(float(wr) * w), int(float(hr) * h)
                if cc == '0':
                    color = (0, 0, 255)
                else:
                    color = (0, 255, 0)
                cv.rectangle(imc, (int(xr - int(wr / 2)), int(yr - int(hr / 2))),
                             (int(xr) + int(wr / 2), int(yr + int(hr / 2))), color=color, thickness=1)
        try:
            if 1:#len(f.split('+')) == 1:  # 被改过的
                cv.imwrite(join(project_dir, 'data', 'view', name_root + '.jpg'), imc)
        except:
            print('Bug', name_root)



def mask_to_label(project_name):
    project_dir = join('project', project_name)
    # More data
    pool = Pool(cpu_count() - 1)
    pool_len = cpu_count() - 1
    # r = pool.map(pcs_img, file_list)

    sample_pool = []
    image_list = os.listdir(join(project_dir, 'data', 'train', 'masks'))
    image_list.sort()
    for sample in tqdm(image_list):
        sample_pool.append([sample, project_dir])
        if len(sample_pool) >= pool_len:
            r = pool.map(mask_to_label_pcs, sample_pool)
            sample_pool = []
    if sample_pool is not []:
        r = pool.map(mask_to_label_pcs, sample_pool)


def make_training_plan(project_name):
    project_dir = join('project', project_name)
    file_list = os.listdir(join(project_dir, 'data', 'train', 'images'))
    f_train = open(join(project_dir, 'model', 'train.txt'), 'w')
    f_test = open(join(project_dir, 'model', 'test.txt'), 'w')
    for f in file_list:
        if random.random() > 0.2:
            f_train.write('%s\n' % join(cwd, project_dir, 'data', 'train', 'images', f))
        else:
            f_test.write('%s\n' % join(cwd, project_dir, 'data', 'train', 'images', f))


def train_detection_check(project_name):
    try:
        project_dir = join('project', project_name)
        error_list = []
        fid = open(join(project_dir, 'model', 'train.txt'), 'r')
        files = fid.readlines()
        train_len = len(files)
        fid.close()

        for f in files:
            f = f.replace('\r', '').replace('\n', '')
            if os.path.exists(f) is False:
                error_list.append(f)
            if os.path.exists(join('/'.join(os.path.split(f)[0].split('/')[:-1]), 'labels', os.path.splitext(os.path.split(f)[1])[0]+'.txt')) is False:
                error_list.append(f)

        fid = open(join(project_dir, 'model', 'test.txt'), 'r')
        files = fid.readlines()
        test_len = len(files)
        fid.close()

        for f in files:
            f = f.replace('\r', '').replace('\n', '')
            if os.path.exists(f) is False:
                error_list.append(f)
            if os.path.exists(join('/'.join(os.path.split(f)[0].split('/')[:-1]), 'labels', os.path.splitext(os.path.split(f)[1])[0]+'.txt')) is False:
                error_list.append(f)

        return error_list, train_len, test_len
    except:
        return -1, -1, -1


def train_classification(project_name, settings, max_step):
    project_dir = join('project', project_name)
    previous_weight = ''
    if max_step != 0:
        previous_weight = join(project_dir, 'weight', '%s_%d.weights' % (project_name, max_step))
    add_epoch_number = input_window(img_bg, 'How many epoch should be added? (Leave empty as default 10000)')
    if add_epoch_number != '':
        max_step += int(add_epoch_number)

    settings['MAX_STEP_100'] = max_step

    learning_rate = input_window(img_bg, 'Set learning rate? (Leave empty as default %f)' % settings['LEARNING_RATE'])
    if learning_rate != '':
        settings['LEARNING_RATE'] = float(learning_rate)

    model_cfg = ''

    gpus = input_window(img_bg, 'GPU? (Leave empty as default 0)')
    if gpus == '':
        gpus = '-gpus 0'
    else:
        gpus = '-gpus %s' % gpus

    if settings['VERSION'].lower() == 'd9':
        # CLASS_NUMBER,  FILTER_NUMBER, LEARNING_RATE,  MAX_STEP
        model_cfg = class_d9

    if settings['VERSION'].lower() == 'd19':
        # CLASS_NUMBER,  FILTER_NUMBER, LEARNING_RATE,  MAX_STEP
        model_cfg = class_d9

    for k in settings.keys():
        if isinstance(settings[k], str) is False:
            model_cfg = model_cfg.replace('{' + k + '}', '{:g}'.format(settings[k]))
        else:
            model_cfg = model_cfg.replace('{' + k + '}', settings[k])

    with open(join(cwd, 'project', project_name, 'model', project_name + '.cfg'), 'w') as fid:
        fid.write('%s' % model_cfg)

    with open(join(cwd, 'project', project_name, 'settings.json_report'), 'w') as fid:
        json_report.dump(settings, fid)

    print('Learning Rate: %f' % settings['LEARNING_RATE'])
    print('Max Epoch: %f' % settings['MAX_STEP_100'])

    start_confirm = input_window(img_bg, 'Start to train?')

    data_file = join(project_dir, 'model', 'data.txt')
    cfg_file = join(project_dir, 'model', '%s.cfg' % project_name)
    if os.path.exists(join(project_dir, 'log')) is False:
        os.mkdir(join(project_dir, 'log'))

    date_str = time.strftime('%Y%m%d%H%M%S', time.localtime())
    log1 = join(project_dir, 'log', 'log.1.%s' % date_str)
    log2 = join(project_dir, 'log', 'log.2.%s' % date_str)

    # ./darknet classifier train cfg/darknet19_ppg.data cfg/darknet_ppg.cfg /home/fc/data/PPG/weight_13/darknet_ppg_400.weights

    if start_confirm.lower() in ['yes', 'y', 'ok']:
        print('Training...')
        print('please check %s and %s' % (log1, log2))
        print('exe/see classifier train %s %s %s %s 1>%s 2>%s' % (data_file, cfg_file, previous_weight, gpus, log1, log2))
        os.system('exe/see classifier train %s %s %s %s 1>%s 2>%s' % (data_file, cfg_file, previous_weight, gpus, log1, log2))


def train(project_name, settings, max_step):

    if settings['VERSION'].lower() in ['v3t', 'v3', 'v4', 'v4t']:
        error_list, train_len, test_len = train_detection_check(project_name)
        if error_list == -1:
            print('Error: Please add and make data.')
            return

        if len(error_list) > 0:
            print('Lack of files:')
            for err in error_list:
                print('    %s' % err)
            return
        elif train_len == 0 or test_len == 0:
            print('No training data.')
            return
        else:
            print('Train set number: %d, test set number: %d' % (train_len, test_len))
            print('Trained epoch: %d' % (max_step))

            project_dir = join('project', project_name)
            train_detection(project_name, settings, max_step)

    if settings['VERSION'].lower() in ['d9', 'd19']:
        train_classification(project_name, settings, max_step)


def train_detection(project_name, settings, max_step):
    project_dir = join('project', project_name)
    previous_weight = ''
    if max_step != 0:
        previous_weight = join(project_dir, 'weight', '%s_%d.weights' % (project_name, max_step))
    add_epoch_number = input_window(img_bg, 'How many epoch should be added? (Leave empty as default 10000)')
    if add_epoch_number != '':
        max_step_90 = max_step + int(int(add_epoch_number) * 0.9)
        max_step_80 = max_step + int(int(add_epoch_number) * 0.8)
        max_step += int(add_epoch_number)
    else:
        max_step_90 = max_step + 9000
        max_step_80 = max_step + 8000
        max_step += 10000

    settings['MAX_STEP_100'] = max_step
    settings['MAX_STEP_80'] = max_step_80
    settings['MAX_STEP_90'] = max_step_90

    learning_rate = input_window(img_bg, 'Set learning rate? (Leave empty as default %f)' % settings['LEARNING_RATE'])
    if learning_rate != '':
        settings['LEARNING_RATE'] = float(learning_rate)

    model_cfg = ''

    gpus = input_window(img_bg, 'GPU? (Leave empty as default 0)')
    if gpus == '':
        gpus = '-gpus 0'
    else:
        gpus = '-gpus %s' % gpus

    if settings['VERSION'].lower() == 'v4':
        # CLASS_NUMBER,  FILTER_NUMBER, LEARNING_RATE,  MAX_STEP
        model_cfg = yolo_v4

    if settings['VERSION'].lower() == 'v3t':
        # CLASS_NUMBER,  FILTER_NUMBER, LEARNING_RATE,  MAX_STEP
        model_cfg = yolo_v3_tiny

    if settings['VERSION'].lower() == 'v4t':
        # CLASS_NUMBER,  FILTER_NUMBER, LEARNING_RATE,  MAX_STEP
        model_cfg = yolo_v4_tiny


    for k in settings.keys():
        if isinstance(settings[k], str) is False:
            model_cfg = model_cfg.replace('{' + k + '}', '{:g}'.format(settings[k]))
        else:
            model_cfg = model_cfg.replace('{' + k + '}', settings[k])

    with open(join(cwd, 'project', project_name, 'model', project_name + '.cfg'), 'w') as fid:
        fid.write('%s' % model_cfg)

    with open(join(cwd, 'project', project_name, 'settings.json_report'), 'w') as fid:
        json_report.dump(settings, fid)

    print('Learning Rate: %f' % settings['LEARNING_RATE'])
    print('Max Epoch: %f' % settings['MAX_STEP_100'])

    start_confirm = input_window(img_bg, 'Start to train?')

    # detector train data/metaldot.data ../metaldot/model/yolov4_metaldot_rs.cfg ../metaldot/weight/yolov4_metaldot_25000.weights  -gpus 0

    data_file = join(project_dir, 'model', 'data.txt')
    cfg_file = join(project_dir, 'model', '%s.cfg' % project_name)
    if os.path.exists(join(project_dir, 'log')) is False:
        os.mkdir(join(project_dir, 'log'))

    date_str = time.strftime('%Y%m%d%H%M%S', time.localtime())
    log1 = join(project_dir, 'log', 'log.1.%s' % date_str)
    log2 = join(project_dir, 'log', 'log.2.%s' % date_str)

    if start_confirm.lower() in ['yes', 'y', 'ok']:
        print('Training...')
        print('please check %s and %s' % (log1, log2))
        print('exe/see detector train %s %s %s %s 1>%s 2>%s' % (data_file, cfg_file, previous_weight, gpus, log1, log2))
        os.system('exe/see detector train %s %s %s %s 1>%s 2>%s' % (data_file, cfg_file, previous_weight, gpus, log1, log2))
        #os.system('exe/see detector train %s %s %s %s' % (data_file, cfg_file, previous_weight, gpus))


def make_detection_data(project_name, samples, settings):
    sample_list = []
    for sam2 in samples:
        for sample in sam2:
            sample_list.append(sample)
    print('Make training data:')
    make_data(project_name, sample_list)
    print('Mask to label:')
    mask_to_label(project_name)
    print('Make training plan.')
    make_training_plan(project_name)


def make_classification_data(project_name, samples, settings):
    class_rate_str = input_window(img_bg, 'Input the rate of each class (%s) [eg:0.9,0.8,1,0...] (leave empty for all 1):\n' % settings['CLASSES'])
    classes = settings['CLASSES'].split(',')
    class_rate = {}

    if class_rate_str != '':
        while True:
            if len(class_rate_str.split(',')) != len(classes):
                class_rate_str = input_window(img_bg, 'Input the rate of each class (%d) [eg:0.9,0.8,1,0...]:\n' % settings[
                    'CLASSES'])
                continue

            for i, r in enumerate(class_rate_str.split(',')):
                try:
                    if float(r) < 0 or float(r) > 1:
                        class_rate_str = input_window(img_bg,
                                                      'Input the rate of each class (%d) [eg:0.9,0.8,1,0...]:\n' % settings[
                                                          'CLASSES'])
                        continue

                    class_rate[classes[i]] = float(r)
                except:
                    class_rate_str = input_window(img_bg,
                                                  'Input the rate of each class (%d) [eg:0.9,0.8,1,0...]:\n' % settings[
                                                      'CLASSES'])
                    continue
            break
    else:
        for i, r in enumerate(classes):
            class_rate[classes[i]] = 1

    whole_list = []

    for i, r in enumerate(classes):
        for sample in samples[r]:
            if class_rate[r] > random.random():
                whole_list.append(sample)

    random.shuffle(whole_list)

    print('Total training data number: %d' % len(whole_list))

    project_dir = join('project', project_name)


    f_train = open(join(project_dir, 'model', 'train.txt'), 'w')
    f_test = open(join(project_dir, 'model', 'test.txt'), 'w')
    for f in whole_list:
        if random.random() > 0.2:
            f_train.write('%s\n' % join(cwd, f))
        else:
            f_test.write('%s\n' % join(cwd, f))



#start seletect
def main():
    project_name = input_window(img_bg, 'Input project name to create a new project, \nor [ENTER] directly to select a existed project:')
    if project_name == '':
        file_list = os.listdir('project')
        project_list = []
        for p in file_list:
            if os.path.isdir(join('project', p)):
                project_list.append(p)

        if len(project_list) == 0:
            print('No project is existed. Bye.')
            return

        print('List all the project (%d):' % len(project_list))
        project_list.sort()
        for i, p in enumerate(project_list):
            print('[%d] %s' % (i + 1, p))

        selected_project_index = -1
        while not (0 < selected_project_index <= len(project_list)):
            selected_project_index = int(input_window(img_bg, 'Select one project'))

        selected_operation = 0

        while selected_operation >= 0:
            print('----Operations----')
            print('[1] Check project')
            print('[2] Check, and make raw data to training data')
            print('[3] Train the model')
            print('[4] Check, make data and train')
            print('[0] Exit')
            selected_operation = int(input_window(img_bg, 'What do you want to do?'))
            project_name = project_list[selected_project_index - 1]
            if selected_operation == 0:
                return
            if selected_operation == 1:
                check_project(project_name)
            if selected_operation == 2:
                samples, settings, max_step = check_project(project_list[selected_project_index - 1])
                if settings['VERSION'].lower() in ['v3', 'v3t', 'v4', 'v4t']:
                    make_detection_data(project_name, samples, settings)

                if settings['VERSION'].lower() in ['d9', 'd19']:
                    make_classification_data(project_name, samples, settings)

            if selected_operation == 3:
                samples, settings, max_step = check_project(project_list[selected_project_index - 1])
                train(project_list[selected_project_index - 1], settings, max_step)

    else:
        if os.path.exists(join('.', 'project', project_name)) is True:
            print('The proposed project name is existed. Bye.')
            return
        create_new_project(project_name)


if __name__ == '__main__':
    mp.set_start_method('spawn')
    main()
