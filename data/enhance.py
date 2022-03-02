import cv2  # 引入opencv 的库
import os
from data.labels_ import read_label
import uuid
# import dots_cut
import argparse
import logging
from data import dots_cut
import shutil
from tqdm import tqdm


def enhance(img_path, labels_path, save_path):
    """
    数据增强

    这个功能进行了以下操作(目前是对数据进行2倍数据增强，如果想要多倍，可在enhance.py中更改num的数字)：
    1. 有白框的图片先沿白框边裁剪1次；在白框到原图边界的的距离范围中随机再次裁剪1次
    2. 无白框的图片：在所有目标的最小外接矩形到原图边界的的距离范围中随机裁剪2次
    生成的文件为：
    1. images(是最终训练所使用的图片，包括原图与增强后的图片，图片名为：'原图名_enhancedi.jpg'，i为随机裁剪的次数(i=1或者i=2))
    2. labels(是最终训练所使用的标签，包括原图与增强后的标签，标签名为：'原标签名_enhancedi.txt')
    3. log：记录数据增强函数的日志，内容为:原图名、有无白框判断、裁剪参数(记录随机生成的参数：(0~x的最小值到),(0~y的最小值到),(x的最大值到图片的宽),(Y的最大值到图片的高))

    Parameters
    ----------
    images_path : str
        输入根据关键词合成后的数据集生成的images文件夹的地址
    label_path : str
        输入转换好的labels的文件夹地址
    save_to : str
        输入数据增强后所有文件的保存地址(包括
    log_save_to : str
        输入数据增强后的log文件的保存地址

    Return
    ------
    flag : int
        返回 flag = 0 未进行数据增强或者 flag = 1 进行了数据增强
    """

    def cut_images(img_path, save_img_path, save_label_path, labels_path, flag, i):  # ./images/
        # 找到白框点
        result = ''
        res_img_path, res_label_path = '', ''
        xs, ys = dots_cut.point(img_path)  # ../1.jpg
        img_oriname = img_path.split('/')[-1]  # 1.jpg
        img_name = os.path.splitext(img_oriname)[0]
        save_filename = img_name + '_enhanced' + str(i + 1)
        uuid_ = uuid.uuid4()
        # print(xs, ys)

        if -1 in xs or -1 in ys:
            # print('无白框')
            # 原图无白框，随机裁取
            l = read_label(labels_path)  # 以元组返回((x_small,x/w), (y_small,y/h), (x_big,x/w), (y_big,y/h), line_list)
            # print(labels_path,l)
            img = cv2.imread(img_path, 1)  # 三通道
            # 存入图片
            # name = str(uuid_)
            name = save_filename
            result = dots_cut.cut_(l, img, save_img_path, name, save_label_path)
            # print('结果：',result)
            res_img_path = save_img_path + name + '.jpg'
            res_label_path = save_label_path + name + '.txt'
            flag = 0
        else:
            # 有白框，先裁取
            # labels 文件名
            # 读取labels并返回 x_min, y_min, x_max, y_max, line_list
            l = read_label(labels_path)
            name = save_filename
            # print('有')
            if l == []:
                # label为空
                # name = str(uuid_)
                result = dots_cut.cut(name + '.jpg', img_path, xs, ys, save_img_path)
                # open(save_label_path + name + '.txt', "w")
                with open(os.path.join(save_label_path, f"{name}{'.txt'}"), "w") as f:
                    f.write('')
                res_img_path = save_img_path + name + '.jpg'
                res_label_path = save_label_path + name + '.txt'
                flag = 1
            else:
                # x_min, y_min, x_max, y_max
                l0, l1, l2, l3 = float(l[0][0]), float(l[1][0]), float(l[2][0]), float(l[3][0])
                # 读取图片
                img = cv2.imread(img_path, 1)
                # 图片size
                y, x = img.shape[0:2]
                # 裁剪后图片size
                x_new = x - (xs[0] + (x - xs[1]))
                y_new = y - (ys[0] + (y - ys[1]))
                min_x1, min_y1, max_x2, max_y2 = l0 * x, l1 * y, l2 * x, l3 * y
                min_x1_ = min_x1 - (float(l[0][1]) * x) / 2
                min_y1_ = min_y1 - (float(l[1][1]) * y) / 2
                max_x2_ = max_x2 + (float(l[2][1]) * x) / 2
                max_y2_ = max_y2 + (float(l[3][1]) * y) / 2

                if xs[0] < min_x1_ and ys[0] < min_y1_ and xs[1] > max_x2_ and ys[1] > max_y2_:
                    for point in l[4]:
                        x_ = str((float(point[1]) * x - xs[0]) / x_new)
                        y_ = str((float(point[2]) * y - ys[0]) / y_new)
                        w_ = str((float(point[3]) * x) / x_new)
                        h_ = str((float(point[4]) * y) / y_new)
                        # print(x_, y_,w_,h_)
                        labels_ = point[0] + ' ' + x_ + ' ' + y_ + ' ' + w_ + ' ' + h_ + '\n'
                        with open(save_label_path + name + '.txt', 'a') as f:
                            f.write(labels_)
                    result = dots_cut.cut(name + '.jpg', img_path, xs, ys, save_img_path)
                    res_img_path = save_img_path + name + '.jpg'
                    res_label_path = save_label_path + name + '.txt'
                    flag = 1

        return res_img_path, res_label_path, flag, result
        # except Exception as e:
        #     print(e)

    def choose_num(num, img_path, labels_path, save_path):
        save_img_path = save_path + 'images/'
        if not os.path.exists(save_img_path):
            os.mkdir(save_img_path)
        save_label_path = save_path + 'labels/'
        if not os.path.exists(save_label_path):
            os.mkdir(save_label_path)
        for root, dirs, files in os.walk(img_path):  # 这里就填文件夹目录就可以了
            for file in tqdm(files):
                flag = 0

                shutil.copy(os.path.join(root, file), os.path.join(save_img_path, file))  # 复制原图
                shutil.copy(os.path.join(labels_path, file[:-4] + '.txt'),
                            os.path.join(save_label_path, file[:-4] + '.txt'))  # 复制标签

                res_img_path, res_label_path = '', ''
                for i in range(num):
                    if '.jpg' in file:
                        img_path_ = os.path.join(root, file)
                        labels_path_ = os.path.join(labels_path, file[:-4] + '.txt')
                        ori_img = '原图：' + file
                        logging.critical(ori_img)
                        if res_img_path != '' or res_label_path != '':
                            # print(res_img_path, res_label_path)
                            result_img = '裁剪后的图片' + res_img_path
                            result_label = '裁剪后的label' + res_label_path
                            logging.critical(result_img)
                            logging.critical(result_label)

                            # logging.critical(res_img_path)
                            # logging.critical(res_label_path)
                        # print(file)

                        # print(flag)
                        # logging.critical(flag)
                        if flag == 0:  # 无白框
                            opt = '无白框' + str(flag)
                            logging.critical(opt)
                            res_img_path, res_label_path, flag, result = cut_images(img_path_, save_img_path,
                                                                                    save_label_path,
                                                                                    labels_path_, flag, i)
                            save_result = '裁剪参数((x_small,随机0~x_samll),(y_small,随机0~y_samll),(x_max,随机x_max~w),(y_max,随机y_max~h)):' + str(
                                result)
                            logging.critical(save_result)
                        elif flag == 1:
                            opt = '有白框' + str(flag)
                            logging.critical(opt)
                            res_img_path, res_label_path, flag, result = cut_images(res_img_path, save_img_path,
                                                                                    save_label_path,
                                                                                    res_label_path, flag, i)
                            save_result = '裁剪参数((x_small,随机0~x_samll),(y_small,随机0~y_samll),(x_max,随机x_max~w),(y_max,随机y_max~h)):' + str(
                                result)
                            logging.critical(save_result)

    # if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='Personal information')
    # parser.add_argument('--img_path', dest='img_path', type=str)
    # parser.add_argument('--labels_path', dest='labels_path', type=str)
    # parser.add_argument('--save_path', dest='save_path', type=str)
    # parser.add_argument('--num', dest='num', type=int)
    # args = parser.parse_args()
    # if not os.path.exists(args.save_path):
    #     os.mkdir(args.save_path)
    # choose_num(args.num, args.img_path, args.labels_path, args.save_path)

    # img_path = '/media/vs/Data/aist/project/helmet/images/'
    # labels_path = '/media/vs/Data/aist/project/helmet/labels/'
    # save_path = '/media/vs/Data/aist/project/helmet/save_images/'
    num = 2
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    save_log = save_path + 'log/'
    if not os.path.exists(save_log):
        os.mkdir(save_log)
    log_path = save_log + 'cut_img.log'
    logging.basicConfig(level=logging.DEBUG,  # 控制台打印的日志级别
                        filename=log_path,
                        filemode='a',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                        # a是追加模式，默认如果不写的话，就是追加模式
                        format=
                        '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                        # 日志格式
                        )
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    choose_num(num, img_path, labels_path, save_path)

# save_path = '/media/vs/qi/data/test2/test/images_save/'
# if os.path.exists(save_path):
#     shutil.rmtree(save_path)
# save_path = save_pa + '/'
# enhance('/media/vs/qi/data/test2/test/images/','/media/vs/qi/data/test2/test/labels/',save_path)
