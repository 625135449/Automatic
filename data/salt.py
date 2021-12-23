import numpy as np
import cv2
import os
import shutil
from matplotlib import pyplot as plt

# def addsalt_pepper(img, SNR):
#     img_ = img.copy()
#     c, h, w = img_.shape
#     mask = np.random.choice((0, 1, 2), size=(1, h, w), p=[SNR, (1 - SNR) / 2., (1 - SNR) / 2.])
#     mask = np.repeat(mask, c, axis=0)     # 按channel 复制到 与img具有相同的shape
#     img_[mask == 1] = 255    # 盐噪声
#     img_[mask == 2] = 0      # 椒噪声
#
#     return img_
#
#
# img = cv2.imread('/media/vs/qi/data/task/lift_white/20210701102026.jpg')
#
# SNR_list = [0.9, 0.7, 0.5, 0.3]
# sub_plot = [221, 222, 223, 224]
#
# plt.figure(1)
# for i in range(len(SNR_list)):
#     plt.subplot(sub_plot[i])
#     # img_s = addsalt_pepper(img.transpose(2, 1, 0), SNR_list[i])     # c,
#     img_s = addsalt_pepper(img.transpose(2, 1, 0), 0.05)
#     img_s = img_s.transpose(2, 1, 0)
#     cv2.imshow('PepperandSalt', img_s)
#     cv2.waitKey(0)
#     plt.imshow(img_s[:,:,::-1])     # bgr --> rgb
#     plt.title('add salt pepper noise(SNR={})'.format(SNR_list[i]))
#
# plt.show()
def salt(ori_p,save_imgpath,label_path):
    def SaltAndPepper(src,percetage=0.05):
        SP_NoiseImg=src.copy()
        SP_NoiseNum=int(percetage*src.shape[0]*src.shape[1])
        for i in range(SP_NoiseNum):
            randR=np.random.randint(0,src.shape[0]-1)
            randG=np.random.randint(0,src.shape[1]-1)
            randB=np.random.randint(0,3)
            if np.random.randint(0,1)==0:
                SP_NoiseImg[randR,randG,randB]=0
            else:
                SP_NoiseImg[randR,randG,randB]=255
        return SP_NoiseImg

    for root ,dirs,files in os.walk(save_imgpath):
        for name in files:
            img_path = os.path.join(root,name)
            img = cv2.imread(img_path)  # 椒盐
            img_salt = SaltAndPepper(img, 0.05)
            save_p = ori_p + '/enhance'
            if not os.path.exists(save_p):
                os.mkdir(save_p)
            save_img = save_p + '/images'
            if not os.path.exists(save_img):
                os.mkdir(save_img)
            save_lb = save_p + '/labels'
            if not os.path.exists(save_lb):
                os.mkdir(save_lb)
            cv2.imwrite(save_img+'/'+name[:-4]+'salt.jpg', img_salt)
            shutil.copy(os.path.join(label_path, name[:-4] + '.txt'), os.path.join(save_lb, name[:-4] + 'salt.txt'))
            shutil.copy(os.path.join(root, name), os.path.join(save_img, name))  # 复制原图
            shutil.copy(os.path.join(label_path, name[:-4] + '.txt'), os.path.join(save_lb, name[:-4] + '.txt'))  # 复制标签
        print('ok')


    # img = cv2.imread('/media/vs/qi/data/task/lift_white/20210701102026.jpg')
    # img_salt = SaltAndPepper(img, 0.05)
    # cv2.imwrite('/media/vs/qi/data/task/lift_white/2.jpg', img_salt)
salt('/media/vs/Data/aist/project/helmet_20210719','/media/vs/Data/aist/project/helmet_20210719/save/images','/media/vs/Data/aist/project/helmet_20210719/save/labels')