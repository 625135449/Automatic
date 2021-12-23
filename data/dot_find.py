import cv2 as cv
import numpy as np
from os.path import join
import os


def find_dot(img_path):
    im = cv.imread(img_path)
    match_dot_number = 5
    im_ori_ = im.copy()
    im_ori = im.copy()
    im_b = im[:, :, 0]
    im_g = im[:, :, 1]
    im_r = im[:, :, 2]

    im_b[im_b < 200] = 0
    im_g[im_g < 200] = 0
    im_r[im_r < 200] = 0

    im = im_b * im_g * im_r

    im = im.astype(np.int16)
    # cv.imshow('1', im)
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
    xs = find_two(vote(x_coor_set, 1))
    ys = find_two(vote(y_coor_set, 0))

    #
    # print(vote(x_coor_set, 1))
    # print(vote(y_coor_set, 0))

    cv.rectangle(im_ori_, (xs[0], ys[0]), (xs[1], ys[1]), (0, 255, 0), thickness=1)
    # print(xs[0], ys[0])
    # print(xs[1], ys[1])
    newimg = im_ori[ys[0]:ys[1], xs[0]:xs[1]]
    cv.imshow('out', im_ori_)
    cv.imwrite('./save/' + '8.jpg', newimg)
    cv.waitKey(0)
    # return xs, ys


def vote(coor_set, index):
    vote_dict = {}
    for x in coor_set:
        x_value = x[index]
        x_list = list(vote_dict.keys())
        if len(x_list) == 0:
            vote_dict[x_value] = 1
        else:
            diff = min(np.abs(np.array(x_list) - x_value))
            if diff > 5:
                vote_dict[x_value] = 1
            else:
                vote_dict[x_value] += 1
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


if __name__ == "__main__":
    # n = find_dot(r'./save_images/images/ddd30f5f-58d1-452b-91f8-3078497e9d5b.jpg')
    n = find_dot(r'/home/fei/Desktop/images/7.jpg')
    # print(n)
