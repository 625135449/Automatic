import cv2 as cv
import numpy as np
import random
import os


def point(img):
    match_dot_number = 5
    im = cv.imread(img)
    im_ori = im.copy()
    # 分别获取图片的 BGR 颜色（cv）
    im_b = im[:, :, 0]
    im_g = im[:, :, 1]
    im_r = im[:, :, 2]

    im_b[im_b < 200] = 0
    im_g[im_g < 200] = 0
    im_r[im_r < 200] = 0

    im = im_b * im_g * im_r
    im = im.astype(np.int16)

    im[im != 0] = 1
    im[im == 0] = -1
    pattern = []

    for i in range(match_dot_number):
        pattern.extend([1, 1, 1, 1, 1])
        for j in range(15):
            pattern.append(-1)

    imgkernel = np.array([pattern])
    imgkernel = imgkernel.T

    # dst1 用来找X坐标
    dst1 = cv.filter2D(im, -1, imgkernel)
    dst2 = cv.filter2D(im, -1, imgkernel.T)

    dst1[dst1 < match_dot_number * 20 - 2] = 0
    dst1[dst1 >= match_dot_number * 20 - 2] = 255
    dst1 = dst1.astype(np.uint8)

    dst2[dst2 < match_dot_number * 20 - 2] = 0
    dst2[dst2 >= match_dot_number * 20 - 2] = 255
    dst2 = dst2.astype(np.uint8)

    x_coor_set = np.argwhere(dst1 == 255)
    y_coor_set = np.argwhere(dst2 == 255)

    def vote(coor_set, index):
        vote_dict = {}
        for x in coor_set:
            x_value = x[index]
            x_list = list(vote_dict.keys())
            if len(x_list) == 0:
                vote_dict[x_value] = 1
            else:
                try:
                    diff = min(np.abs(np.array(x_list) - x_value))
                    if diff > 5:
                        vote_dict[x_value] = 1
                    else:
                        vote_dict[x_value] += 1
                except KeyError:
                    continue
        return vote_dict

    def find_two(d):
        l = []
        for k, v in d.items():
            l.append([k, v])
        l.sort(key=lambda x: x[1], reverse=True)
        if len(l) < 2:
            return -1, -1
        l = [l[0][0], l[1][0]]
        l.sort()
        return l

    xs = find_two(vote(x_coor_set, 1))
    ys = find_two(vote(y_coor_set, 0))
    # print(xs, ys)
    return xs, ys


def cut(img_file, img, xs, ys, save_path):
    def cut1(img, xs, ys):
        # 从轮廓出裁剪图片
        x1, y1 = xs[0], ys[0]  # 获取左上角坐标
        x2, y2 = xs[1], ys[1]  # 获取右下角坐标
        img_cut = img[y1:y2, x1:x2]  # 切片裁剪图像
        return img_cut

    img = cv.imread(img)
    if -1 in xs or -1 in ys:
        cv.imwrite(save_path + img_file, img)
    else:
        img_cut = cut1(img, xs, ys)
        cv.imwrite(save_path + img_file, img_cut)


def cut_(l, img, save_path, img_file, save_label_path):
    min_x1_T, max_x2_T, xs1_,min_y1_T, max_y2_T, ys1_ ='','','','','',''
    if l == []:
        # 原图size
        y, x = img.shape[0:2]
        xs0 = int(choose_())
        xs1 = x - int(choose_())
        ys0 = int(choose_())
        ys1 = y - int(choose_())
        if ys0 < ys1 and xs0 < xs1:
            newimg = img[ys0:ys1, xs0:xs1]
            cv.imwrite(save_path + img_file + '.jpg', newimg)

            with open(os.path.join(save_label_path, f"{img_file}{'.txt'}"), "w") as f:
                f.write('')
            # open(save_label_path + img_file + '.txt', "w")
    else:
        # label 中心点（l0,l1）宽 l3 长：l2
        l0, l1, l2, l3 = float(l[0][0]), float(l[1][0]), float(l[2][0]), float(l[3][0])   #x_s,y_s,x_b,y_b
        # 原图size h,w
        y, x = img.shape[0:2]
        # print(y, x)
        min_x1, min_y1, max_x2, max_y2 = l0 * x, l1 * y, l2 * x, l3 * y   #原尺寸
        min_x1_ = min_x1 - (float(l[0][1]) * x) / 2  #xleft_min
        min_y1_ = min_y1 - (float(l[1][1]) * y) / 2  #yleft_min
        max_x2_ = max_x2 + (float(l[2][1]) * x) / 2  #xright_max
        max_y2_ = max_y2 + (float(l[3][1]) * y) / 2  #yright_max

        # d = b if a else c  #如果a为真，结果是b，否则结果是c
        min_x1_T = min_x1_ if min_x1_ > 0 else 0   #判断超出图片范围的标签
        min_y1_T = min_y1_ if min_y1_ > 0 else 0
        max_x2_T = max_x2_ if max_x2_ < x else x
        max_y2_T = max_y2_ if max_y2_ < y else y
        xs0 = int(choose(min_x1_T))   #new xleft
        ys0 = int(choose(min_y1_T))  #判断像素,随机生成一个
        xs1_ = int(choose(x - max_x2_T))
        ys1_ = int(choose(y - max_y2_T))
        xs1 = int(xs1_ + max_x2_T)    #new xright
        ys1 = int(ys1_ + max_y2_T)
        x_new = x - (xs0 + (x - xs1)) #裁剪后的w
        y_new = y - (ys0 + (y - ys1))

        if xs0 < min_x1_T and ys0 < min_y1_T and xs1 > max_x2_T and ys1 > max_y2_T:
            for point_ in l[4]:
                x_ = str((float(point_[1]) * x - xs0) / x_new)
                y_ = str((float(point_[2]) * y - ys0) / y_new)
                w_ = str((float(point_[3]) * x) / x_new)
                h_ = str((float(point_[4]) * y) / y_new)
                labels_ = point_[0] + ' ' + x_ + ' ' + y_ + ' ' + w_ + ' ' + h_ + '\n'
                with open(save_label_path + img_file + '.txt', 'a')as f:
                    f.write(labels_)
            newimg = img[ys0:ys1, xs0:xs1]   #[y0:y1, x0:x1]
            cv.imwrite(save_path + img_file + '.jpg', newimg)
    # return (img_file,xs0/x,ys0/y,xs1/x,ys1/y),(img_file,xs0,ys0,xs1,ys1)
    return (min_x1_T,xs0),(max_x2_T,xs1_),(min_y1_T,ys0),(max_y2_T,ys1_)


def choose(value):
    threshold1, threshold2, threshold3, threshold4 = [0, 2], 50, 100, 200
    if threshold1[0] <= value <= threshold1[1]:
        res = value
    elif threshold1[1] <= value <= threshold2: #2-50
        res = random.randint(threshold1[1], int(value))   # a <= n <= b.整数
    elif threshold2 <= value <= threshold3: #50-100
        res = random.randint(threshold2, int(value))
    elif threshold3 <= value <= threshold4:  #100-200
        res = random.randint(threshold2, int(value))
    else:  #>200  50<=res<=300
        # res = random.randint(threshold2, 300)
        res = random.randint(threshold4, int(value))
    return res


def choose_():
    res = random.randint(10, 300)
    return res

#
# def cut_all(l, img):
#     def label_(l_, img_):
#         x, y = img_.shape[0:2]
#         x_, w_ = float(l_[1]) * x, float(l_[3]) * x
#         y_, h_ = float(l_[2]) * y, float(l_[4]) * y
#         l = [x_, y_, w_, h_]
#         # print(type(l))
#         return l
#
#     labels_s = []
#     for i in l[4]:
#         # x_, y_, w_, h_ = label_(i, img)
#         l__ = label_(i, img)
#         print(l__[0], type(l__[1]))
#         # print(x_, y_, w_, h_)
#         # labels_s.append(x_)


# if __name__ == "__main__":
    #     # open('test_.txt', 'w')
    #     import os
    #     path = './save_img/'
    #     if not os.path.exists(path):
    #         os.mkdir(path)
    #     save_path = path + '1/'
    #     if not os.path.exists(save_path):
    #         os.mkdir(save_path)
    #     num = 2
    #     img_path = './image'
    #     for root, dirs, files in os.walk(img_path):  # 这里就填文件夹目录就可以了
    #         for file in files:
    #             for flag in range(num):
    #                 if '.jpg' in file:
    #                     print(file)
    # import labels_
    #
    # l = labels_.read_label(r'/home/fei/file_w/code/Data_enhance/label/ee61c210-240f-4fdd-9c06-834fbe30be81.txt')
    # img = cv.imread(r'/home/fei/file_w/code/Data_enhance/image/ee61c210-240f-4fdd-9c06-834fbe30be81.jpg')
    # cut_all(l, img)
