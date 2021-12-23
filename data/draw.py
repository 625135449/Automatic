import os
import cv2
from data.puttext import puttext
import random
from tqdm import tqdm
from time import sleep


def draw_label(num, path, ori_img, save_path):
    # path = input('input label path(../labels):')                  #"/media/vs/Data/darknet_train_result/Truck0406/labels2"  #label address
    # path1 = input('input images path(../images):')                # "/media/vs/Data/darknet_train_result/Truck0406/Truck0406"  #pictures address
    # path2 = input('input drawed iamges path(../val_images):')      #"/media/vs/Data/darknet_train_result/Truck0406/test"   #drawed pictures address

    path = path + '/labels'
    path1 = ori_img
    # path1 = ori_img + '/images'
    path2 = save_path + '/val'

    img_list = os.listdir(path1)
    if not os.path.exists(path2):
        os.makedirs(path2)
    for root, dirs, files in os.walk(path):
        # n = int(len(files)*0.2)
        result = random.sample(files, 10)
        for name in tqdm(result):
            if name.endswith(".txt"):
                filename = root + "/" + name  # /media/wst/Data/darknet训练结果/darknet训练结果/TruckCover/darknet_275_closetransportation/train/labels/31801994.txt
                file_name = name.split('.')[0]  # name = 31801994.txt      file_name = 31801994

                file_path = ''
                file_p = file_name + ".png"
                file_j = file_name + ".jpg"
                file_e = file_name + ".jpeg"
                # print(file_p)
                if file_p in img_list:
                    file_path = path1 + "/" + file_p
                if file_j in img_list:
                    file_path = path1 + "/" + file_j
                if file_e in img_list:
                    file_path = path1 + "/" + file_e

                # file_path = path1 + "/" + file_name + ".jpg"        #label对应的图片

                img = cv2.imread(file_path)  # 读入图片
                h, w = img.shape[:2]
                f = open(filename, "r")
                for each_line in f:
                    each_line_list = each_line.split()  # 将每一行的数字分开放在列表中   1 0.858911 0.570299 0.276238 0.314587   类别，中心点，宽比，高比
                    xmin = (float(each_line_list[1]) - (1 / 2) * (float(each_line_list[3]))) * w
                    ymin = (float(each_line_list[2]) - (1 / 2) * (float(each_line_list[4]))) * h
                    xmax = (float(each_line_list[1]) + (1 / 2) * (float(each_line_list[3]))) * w
                    ymax = (float(each_line_list[2]) + (1 / 2) * (float(each_line_list[4]))) * h

                    cls = str(each_line_list[0])
                    c1, c2 = (int(xmin), int(ymin)), (int(xmax), int(ymax))
                    #####test   bgr
                    # if num == '1':    #GDT_TRUCK
                    #     if cls == '1':           #close
                    #         cv2.rectangle(img, c1,c2,(128, 0, 0), 2)
                    #         img = puttext(img, '密闭', (c1),(128, 0, 0), 20,'yuyang.ttf', "BL")
                    #     if cls == '2':  #OPEN
                    #         cv2.rectangle(img, c1,c2,(0, 128,160), 2)
                    #         img = puttext(img, '打开',(c1), (0, 128,160), 20, 'yuyang.ttf',"BL")
                    #     if cls == '3':  #Incomplete close
                    #         cv2.rectangle(img, c1,c2, (192, 192, 64), 2)
                    #         img = puttext(img, '未带覆盖完全',(c1), (192, 192, 64), 20, 'yuyang.ttf',"BL")
                    #     if cls == '4':  #OTHERS
                    #         cv2.rectangle(img, c1,c2, (0, 128, 64), 2)
                    #         img = puttext(img, '其他类车',(c1), (0, 128, 64), 20, 'yuyang.ttf',"BL")
                    if num == '1':  # CLT
                        if cls == '0':
                            cv2.rectangle(img, c1, c2, (0, 0, 128), 2)
                            img = puttext(img, '车身_货车', (c1), (0, 0, 128), 20, 'yuyang.ttf', "BL")
                        if cls == '1':
                            cv2.rectangle(img, c1, c2, (0, 128, 192), 2)
                            img = puttext(img, '车身_泵车', (c1), (0, 128, 192), 20, 'yuyang.ttf', "BL")
                        if cls == '2':
                            cv2.rectangle(img, c1, c2, (128, 64, 128), 2)
                            img = puttext(img, '车身_挖掘机', (c1), (128, 64, 128), 20, 'yuyang.ttf', "BL")
                        if cls == '3':
                            cv2.rectangle(img, c1, c2, (128, 192, 128), 2)
                            img = puttext(img, '车身_土方车', (c1), (128, 192, 128), 20, 'yuyang.ttf', "BL")
                        if cls == '4':
                            cv2.rectangle(img, c1, c2, (64, 0, 192), 2)
                            img = puttext(img, '车身_面包车', (c1), (64, 0, 192), 20, 'yuyang.ttf', "BL")
                        if cls == '5':
                            cv2.rectangle(img, c1, c2, (64, 192, 128), 2)
                            img = puttext(img, '车身_洒水车', (c1), (64, 192, 128), 20, 'yuyang.ttf', "BL")
                        if cls == '6':
                            cv2.rectangle(img, c1, c2, (192, 64, 192), 2)
                            img = puttext(img, '车身_拖拉机', (c1), (192, 64, 192), 20, 'yuyang.ttf', "BL")
                        if cls == '7':
                            cv2.rectangle(img, c1, c2, (128, 128, 160), 2)
                            img = puttext(img, '车身_三轮摩托车', (c1), (128, 128, 160), 20, 'yuyang.ttf', "BL")
                        if cls == '8':
                            cv2.rectangle(img, c1, c2, (0, 64, 160), 2)
                            img = puttext(img, '车身_摩托车', (c1), (0, 64, 160), 20, 'yuyang.ttf', "BL")
                        if cls == '9':
                            cv2.rectangle(img, c1, c2, (0, 192, 224), 2)
                            img = puttext(img, '车身_搅拌机', (c1), (0, 192, 224), 20, 'yuyang.ttf', "BL")
                        if cls == '10':
                            cv2.rectangle(img, c1, c2, (192, 0, 160), 2)
                            img = puttext(img, '车身_轿车', (c1), (192, 0, 160), 20, 'yuyang.ttf', "BL")
                        if cls == '11':
                            cv2.rectangle(img, c1, c2, (192, 192, 0), 2)
                            img = puttext(img, '货车车斗_有货', (c1), (192, 192, 0), 20, 'yuyang.ttf', "BL")
                        if cls == '12':
                            cv2.rectangle(img, c1, c2, (64, 64, 64), 2)
                            img = puttext(img, '货车车斗_无货', (c1), (64, 64, 64), 20, 'yuyang.ttf', "BL")
                        if cls == '13':
                            cv2.rectangle(img, c1, c2, (0, 160, 0), 2)
                            img = puttext(img, '货车车斗_厢子', (c1), (0, 160, 0), 20, 'yuyang.ttf', "BL")
                        if cls == '14':
                            cv2.rectangle(img, c1, c2, (128, 32, 0), 2)
                            img = puttext(img, '土方车车斗_闭', (c1), (128, 32, 0), 20, 'yuyang.ttf', "BL")
                        if cls == '15':
                            cv2.rectangle(img, c1, c2, (128, 96, 64), 2)
                            img = puttext(img, '土方车车斗_开', (c1), (128, 96, 64), 20, 'yuyang.ttf', "BL")
                        if cls == '16':
                            cv2.rectangle(img, c1, c2, (192, 160, 224), 2)
                            img = puttext(img, '土方车车斗_未完全闭', (c1), (192, 160, 224), 20, 'yuyang.ttf', "BL")
                        if cls == '17':
                            cv2.rectangle(img, c1, c2, (128, 96, 128), 2)
                            img = puttext(img, '车牌_绿牌', (c1), (128, 96, 128), 20, 'yuyang.ttf', "BL")
                        if cls == '18':
                            cv2.rectangle(img, c1, c2, (0, 224, 224), 2)
                            img = puttext(img, '车牌_黄牌', (c1), (0, 224, 224), 20, 'yuyang.ttf', "BL")
                        if cls == '19':
                            cv2.rectangle(img, c1, c2, (192, 64, 64), 2)
                            img = puttext(img, '车牌_蓝牌', (c1), (192, 64, 64), 20, 'yuyang.ttf', "BL")
                        if cls == '20':
                            cv2.rectangle(img, c1, c2, (192, 224, 32), 2)
                            img = puttext(img, '车牌_其他', (c1), (192, 224, 32), 20, 'yuyang.ttf', "BL")
                        if cls == '21':
                            cv2.rectangle(img, c1, c2, (192, 224, 32), 2)
                            img = puttext(img, '车头', (c1), (192, 224, 32), 20, 'yuyang.ttf', "BL")
                        if cls == '22':
                            cv2.rectangle(img, c1, c2, (64, 160, 224), 2)
                            img = puttext(img, '洒水车_洒水', (c1), (64, 160, 224), 20, 'yuyang.ttf', "BL")
                        if cls == '23':
                            cv2.rectangle(img, c1, c2, (192, 160, 128), 2)
                            img = puttext(img, '洒水车_未洒水', (c1), (192, 160, 128), 20, 'yuyang.ttf', "BL")
                        if cls == '24':
                            cv2.rectangle(img, c1, c2, (192, 192, 192), 2)
                            img = puttext(img, '车牌_车身车辆', (c1), (192, 192, 192), 20, 'yuyang.ttf', "BL")
                        if cls == '25':
                            cv2.rectangle(img, c1, c2, (0, 0, 32), 2)
                            img = puttext(img, '冲洗区域', (c1), (0, 0, 32), 20, 'yuyang.ttf', "BL")
                        if cls == '26':
                            cv2.rectangle(img, c1, c2, (64, 192, 192), 2)
                            img = puttext(img, '大门', (c1), (64, 192, 192), 20, 'yuyang.ttf', "BL")
                        if cls == '27':
                            cv2.rectangle(img, c1, c2, (255, 144, 24), 2)
                            img = puttext(img, '车身_拖车', (c1), (255, 144, 24), 20, 'yuyang.ttf', "BL")
                        if cls == '28':
                            cv2.rectangle(img, c1, c2, (128, 0, 64), 2)
                            img = puttext(img, '车身_吊车', (c1), (128, 0, 64), 20, 'yuyang.ttf', "BL")
                        if cls == '29':
                            cv2.rectangle(img, c1, c2, (192, 160, 64), 2)
                            img = puttext(img, '过水池', (c1), (192, 160, 64), 20, 'yuyang.ttf', "BL")
                        if cls == '30':
                            cv2.rectangle(img, c1, c2, (128, 128, 32), 2)
                            img = puttext(img, '土方车车斗_顶棚破损', (c1), (128, 128, 32), 20, 'yuyang.ttf', "BL")
                        if cls == '31':
                            cv2.rectangle(img, c1, c2, (128, 96, 96), 2)
                            img = puttext(img, '冲洗台喷水', (c1), (128, 96, 96), 20, 'yuyang.ttf', "BL")
                        if cls == '32':
                            cv2.rectangle(img, c1, c2, (64, 32, 224), 2)
                            img = puttext(img, '冲洗台未喷水', (c1), (64, 32, 224), 20, 'yuyang.ttf', "BL")
                        if cls == '33':
                            cv2.rectangle(img, c1, c2, (0, 96, 64), 2)
                            img = puttext(img, '车身_工程车', (c1), (0, 96, 64), 20, 'yuyang.ttf', "BL")
                    if num == '2':  # close
                        if cls == '0':  # wear
                            cv2.rectangle(img, c1, c2, (192, 128, 192), 2)
                            img = puttext(img, '车头', (c1), (192, 128, 192), 20, 'yuyang.ttf', "BL")
                        if cls == '1':  # close
                            cv2.rectangle(img, c1, c2, (128, 0, 0), 2)
                            img = puttext(img, '密闭', (c1), (128, 0, 0), 20, 'yuyang.ttf', "BL")
                        if cls == '2':  # OPEN
                            cv2.rectangle(img, c1, c2, (0, 128, 160), 2)
                            img = puttext(img, '打开', (c1), (0, 128, 160), 20, 'yuyang.ttf', "BL")
                        if cls == '3':  # Incomplete close
                            cv2.rectangle(img, c1, c2, (192, 192, 64), 2)
                            img = puttext(img, '未带覆盖完全', (c1), (192, 192, 64), 20, 'yuyang.ttf', "BL")
                        if cls == '4':  # OTHERS
                            cv2.rectangle(img, c1, c2, (0, 128, 64), 2)
                            img = puttext(img, '其他类车', (c1), (0, 128, 64), 20, 'yuyang.ttf', "BL")
                    if num == '3':  # helmet
                        if cls == '1':  # wear
                            cv2.rectangle(img, c1, c2, (0, 128, 0), 2)
                            img = puttext(img, '佩戴安全帽', (c1), (0, 128, 0), 20, 'yuyang.ttf', "BL")
                        if cls == '0':  # no
                            cv2.rectangle(img, c1, c2, (0, 0, 192), 2)
                            img = puttext(img, '未带安全帽', (c1), (0, 0, 192), 20, 'yuyang.ttf', "BL")
                    if num == '4':  # fire
                        if cls == '0':  # wear
                            cv2.rectangle(img, c1, c2, (0, 192, 0), 2)
                            img = puttext(img, '火', (c1), (0, 192, 0), 20, 'yuyang.ttf', "BL")
                        if cls == '1':  # no
                            cv2.rectangle(img, c1, c2, (0, 128, 128), 2)
                            img = puttext(img, '烟', (c1), (0, 128, 128), 20, 'yuyang.ttf', "BL")
                    if num == '5':  # glitter
                        if cls == '1':  # wear
                            cv2.rectangle(img, c1, c2, (0, 0, 192), 2)
                            img = puttext(img, '未穿反光衣', (c1), (0, 0, 192), 20, 'yuyang.ttf', "BL")
                        if cls == '0':  # no
                            cv2.rectangle(img, c1, c2, (0, 128, 0), 2)
                            img = puttext(img, '穿着反光衣', (c1), (0, 128, 0), 20, 'yuyang.ttf', "BL")
                    if num == '6':  # mask
                        if cls == '1':  # wear
                            cv2.rectangle(img, c1, c2, (0, 0, 192), 2)
                            img = puttext(img, '未带口罩', (c1), (0, 0, 192), 20, 'yuyang.ttf', "BL")
                        if cls == '0':  # no
                            cv2.rectangle(img, c1, c2, (0, 128, 0), 2)
                            img = puttext(img, '佩戴口罩', (c1), (0, 128, 0), 20, 'yuyang.ttf', "BL")
                        if cls == '2':  # no
                            cv2.rectangle(img, c1, c2, (192, 192, 64), 2)
                            img = puttext(img, '未佩戴好', (c1), (192, 192, 64), 20, 'yuyang.ttf', "BL")
                    if num == '7':  # proper_glitter
                        if cls == '1':  # wear
                            cv2.rectangle(img, c1, c2, (0, 0, 192), 2)
                            img = puttext(img, '未穿反光衣', (c1), (0, 0, 192), 20, 'yuyang.ttf', "BL")
                        if cls == '0':  # no
                            cv2.rectangle(img, c1, c2, (0, 128, 0), 2)
                            img = puttext(img, '穿着反光衣', (c1), (0, 128, 0), 20, 'yuyang.ttf', "BL")
                        if cls == '2':  # improper
                            cv2.rectangle(img, c1, c2, (192, 96, 224), 2)
                            img = puttext(img, '不规范穿着反光衣', (c1), (192, 96, 224), 20, 'yuyang.ttf', "BL")
                    if num == '8':  # helmet_Glitter
                        if cls == '1':  # wear
                            cv2.rectangle(img, c1, c2, (0, 128, 0), 2)
                            img = puttext(img, '佩戴安全帽', (c1), (0, 128, 0), 20, 'yuyang.ttf', "BL")
                        if cls == '0':  # no
                            cv2.rectangle(img, c1, c2, (0, 0, 192), 2)
                            img = puttext(img, '未带安全帽', (c1), (0, 0, 192), 20, 'yuyang.ttf', "BL")
                        if cls == '2':  # wear
                            cv2.rectangle(img, c1, c2, (0, 0, 192), 2)
                            img = puttext(img, '未穿反光衣', (c1), (0, 0, 192), 20, 'yuyang.ttf', "BL")
                        if cls == '3':  # no
                            cv2.rectangle(img, c1, c2, (0, 128, 0), 2)
                            img = puttext(img, '穿着反光衣', (c1), (0, 128, 0), 20, 'yuyang.ttf', "BL")
                cv2.imwrite(path2 + "/" + file_name + ".jpg", img)
                f.close()
    sleep(0.2)
    print('绘制图片完成')
# draw_label('1','/media/vs/qi/data/test2/test/error','/media/vs/qi/data/test2/test/error/images','/media/vs/qi/data/test2/test/error')
