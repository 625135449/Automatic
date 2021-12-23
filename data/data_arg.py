from PIL import Image #或直接import Image
import os
from data.retangle import pic_rec
import uuid
import shutil
from data.transport import trans
from data.enhance import enhance
from tqdm import tqdm
import numpy as np
import cv2

def arg(path,label_p,save_path):
# path = '/media/vs/Data/aist/project/0712/images'
# #######Input
# label_p = '/media/vs/Data/aist/project/0712/labels'
# save_path = '/media/vs/Data/aist/project/0712/save'

    if not os.path.exists(save_path):
        os.mkdir(save_path)
    save_img = save_path + '/images'
    save_lb = save_path + '/labels'
    if not os.path.exists(save_img):
        os.mkdir(save_img)
    if not os.path.exists(save_lb):
        os.mkdir(save_lb)

    save_img = save_path + '/images'
    save_lb = save_path + '/labels'
    for root ,dirs,files in os.walk(path):    #原图
        for name in tqdm(files):
            img_path = os.path.join(root,name)
            uuid1 = uuid.uuid4()
            img_uuid = str(uuid1) + '.jpg'
            im = Image.open(img_path)
            im1 = im.convert('L')
            uuid2 = uuid.uuid4()
            img_uuid2 = str(uuid2) + '.jpg'

        #     im1.save(os.path.join(save_img,img_uuid2))          ##灰度
        #     shutil.copy(os.path.join(label_p, name[:-4] + '.txt'), os.path.join(save_lb, str(uuid2) + '.txt'))
        #
        #     trans(name,img_path,save_img,label_p,save_lb)      #垂直翻转
        #     img_p,labels_p ,save_p= path + '/',label_p +'/',save_path +'/'
        #
        #     enhance(img_p, labels_p, save_p)     #2裁
        #
        #     pic_rec(name, img_uuid, img_path, save_img, label_p, save_lb)  # 正方形
        #
        #     shutil.copy(os.path.join(root, name), os.path.join(save_img,name))  #复制原图
        #     shutil.copy(os.path.join(label_p, name[:-4] + '.txt'), os.path.join(save_lb,  name[:-4] + '.txt'))  #复制标签
        # print('ok')

            im1.save(os.path.join(save_img, 'gray' + name))  ##灰度 gray
            shutil.copy(os.path.join(label_p, name[:-4] + '.txt'), os.path.join(save_lb, 'gray' + name[:-4] + '.txt'))  #灰度标签

            trans(name, img_path, save_img, label_p, save_lb)  # 垂直翻转 trans

            img_p, labels_p, save_p = path + '/', label_p + '/', save_path + '/'

            enhance(img_p, labels_p, save_p)  # 2裁

            pic_rec(name, img_uuid, img_path, save_img, label_p, save_lb)  # 正方形 ret

            shutil.copy(os.path.join(root, name), os.path.join(save_img, name))  # 复制原图
            shutil.copy(os.path.join(label_p, name[:-4] + '.txt'), os.path.join(save_lb, name[:-4] + '.txt'))  # 复制标签
        print('ok')
