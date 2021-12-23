import os
from os.path import join
import multiprocessing as mp
from data.shuffle import make_test
from data.todarknet_helmet import helmet_reverse
from data.todarknet_json import json_reverse
from data.draw import draw_label
from data.enhance import enhance
from data.data_arg import arg
from tqdm import tqdm
from time import sleep
from data.salt import salt
import os
import cv2
from data.puttext import puttext
import random
from tqdm import tqdm
from time import sleep

img_bg = None


def input_window(img, msg, color='blue'):
    print(msg)
    return input('>')


def main():
    project_name = ''
    if project_name == '':
        file_list = os.listdir('project')
        project_list = []
        for p in file_list:
            if os.path.isdir(join('project', p)):
                project_list.append(p)
        if len(project_list) == 0:
            print('No project is existed. Bye.')
            return
        print('当前路径:', 'project/')
        print('当前文件夹下的所有的文件数量(%d):' % len(file_list))
        project_list.sort()
        for i, p in enumerate(project_list):
            print('[%d] %s' % (i + 1, p))
        selected_project_index = -1
        while not (0 < selected_project_index <= len(project_list)):
            selected_project_index = int(input_window(img_bg, 'Select one project'))

            project_name = project_list[selected_project_index - 1]
            select_path = join('project', project_name)
            project_list1 = []
            print('当前路径:', select_path)  # project/test

            for r, d, f in os.walk(select_path):
                for i in d:
                    if os.path.isdir(join(r, i)):
                        Img_path = join(r, i)
                        if not os.path.exists(join(r, 'images')):
                            os.rename(Img_path, join(r, 'images'))
                        else:
                            break

            file_list1 = os.listdir(select_path)  # 读取所有文件
            for p in file_list1:
                project_list1.append(p)
            if len(project_list1) == 0:
                print('No project is existed. Bye.')
                return
            print('当前文件夹下的所有的文件数量(%d):' % len(file_list1))
            project_list1.sort()

            for i, p in enumerate(project_list1):
                if os.path.isdir(join(select_path, p)):
                    file_list2 = os.listdir(join(select_path, p))
                    print('[%d] %s (%d)' % (i + 1, p, len(file_list2)))
                else:
                    print('[%d] %s' % (i + 1, p))

            selected_project_index1 = -1
            flag = 0
            while not (0 < selected_project_index1 <= len(project_list)):
                selected_project_index1 = int(input_window(img_bg, 'Select one project'))
            selected_operation1 = 0
            while selected_operation1 >= 0:
                print('--------功能菜单--------')
                print('[1] 检查文件数量')
                print('[2] 制作labels')
                print('[3] 制作labels(helmet)')
                print('[4] 标签映射')
                print('[5] 数据增强')
                print('[6] 数据增强(电梯)')
                print('[7] 绘制图片')
                print('[8] 制作测试集')
                print('[0] 退出')
                selected_operation = int(input_window(img_bg, 'What do you want to do?'))
                project_name2 = project_list1[selected_project_index1 - 1]  # pro/test/test.json_report
                select_path2 = join(select_path, project_name2)
                # select = join(select_path, project_list1[0])  # images 第一个
                select = join(select_path, 'images')
                fileList = os.listdir(select_path)  # 读取所有文件
                # save function
                labels_path = select_path + '/labels'
                save_path = select_path + '/save'
                pic = []
                for p in fileList:
                    pic.append(p)
                pic_len = len(pic)
                if selected_operation == 0:
                    return
                if selected_operation == 1:
                    check_project(select_path)
                if selected_operation == 2:
                    json_reverse(pic_len, select_path2, select_path)
                if selected_operation == 3:
                    helmet_reverse(select_path2, select_path)
                if selected_operation == 4:
                    num = input(
                        '1:GDT_truck 2:close_transportation 3:GDT_helmet 4:helmet 5:GDT_fire 6:GDT_glitter 7:GDT_improper_glitter (selecte the num) 8:Helmet_Glitter(Helmet) 9:CLT(30类） 10:广联达CLT 11：FGH(反光衣)')
                    path = select_path + '/labels/'
                    recheck_truckcover(path, num)
                if selected_operation == 5:
                    img_path = select + '/'
                    labels_p = labels_path + '/'
                    save_p = save_path + '/'
                    enhance(img_path, labels_p, save_p)
                    flag = 1
                if selected_operation == 6:
                    # labels_path = select_path + '/labels'
                    # save_path = select_path + '/save'
                    save_img = save_path + '/images'
                    save_lb = save_path + '/labels'
                    arg(select, labels_path, save_path)
                    # salt(select_path,save_img,save_lb)
                    flag = 1
                if selected_operation == 7:
                    option = input('1：绘制全部图片 2：随机绘制十张图片:')
                    num = input(
                        '1:GDT_truck 2:close_transportation 3:helmet 4:fire 5:glitter 6:mask 7:improper glitter 8:Helmet_Glitter(helmet and glitter) 9:CLT 10:烟:11:人')
                    # draw_label(num, select, select_path)
                    if flag == 1 and option == '2':
                        ori_img = save_path + '/images'
                        draw_label(num, save_path, ori_img, save_path)
                        flag = 2
                    else:
                        # draw_label(num, select_path, select, select_path)  # ori_img,save_ori
                        draw(num, select_path, select, select_path)  # ori_img,save_ori
                        flag = 0
                if selected_operation == 8:
                    if flag >= 1:
                        save_img = save_path + '/images'
                        make_test(save_path, save_img)
                        # print(save_path,select)
                    else:
                        make_test(select_path, select)
                # if selected_operation == 9:
                #     train()


def check_project(select_path):
    print('当前路径:', select_path)  # project/test
    file_list3 = os.listdir(select_path)  # 读取所有文件
    project_list3 = []
    for p in file_list3:
        project_list3.append(p)

    if len(file_list3) == 0:
        print('nothing. Bye.')
        return
    else:
        print('当前文件夹下的所有的文件数量(%d):' % len(file_list3))
        project_list3.sort()
        for i, p in enumerate(project_list3):
            if os.path.isdir(join(select_path, p)):
                file_list4 = os.listdir(join(select_path, p))
                print('[%d] %s (%d)' % (i + 1, p, len(file_list4)))
            else:
                print('[%d] %s' % (i + 1, p))

    selected_project_index1 = -1
    while not (0 < selected_project_index1 <= len(project_list3)):
        selected_project_index1 = int(input_window(img_bg, 'Select one project'))
        project_name2 = project_list3[selected_project_index1 - 1]
        select_path2 = join(select_path, project_name2)
        file_list5 = os.listdir(select_path2)  # 读取所有文件
        project_list4 = []
        for p in file_list5:
            project_list4.append(p)

        if len(file_list5) == 0:
            print('nothing. Bye.')
            return
        else:
            print('当前路径:', select_path2)
            print('当前文件夹下的所有的文件数量(%d):' % len(file_list5))
            project_list4.sort()
            for i, p in enumerate(project_list4):
                if os.path.isdir(join(select_path2, p)):
                    file_list6 = os.listdir(join(select_path2, p))
                    print('[%d] %s (%d)' % (i + 1, p, len(file_list6)))
                else:
                    print('[%d] %s' % (i + 1, p))


def recheck_truckcover(path, num):
    for _, _, files in os.walk(path):
        for f in tqdm(files):
            txt_path = os.path.join(path, f)
            with open(txt_path, "r") as f:
                lines = f.readlines()
            result = []
            for i in lines:
                if num == '1':  # GDT_truck
                    if i[0] == None:
                        result.append(None)
                    if i[0] == '0':
                        result.append("2" + i[1:])
                    elif i[1].isdigit():
                        continue
                    elif i[0] == '1':
                        result.append("1" + i[1:])
                    elif i[0] == '2':
                        result.append("3" + i[1:])
                    elif i[0] == '3':
                        result.append("4" + i[1:])
                if num == '2':  # truck
                    if i[0] == None:
                        result.append(None)
                    if i[0] == '0':
                        result.append("0" + i[1:])
                    elif i[1].isdigit():
                        continue
                    elif i[0] == '1':
                        result.append("1" + i[1:])
                    elif i[0] == '2':
                        result.append("2" + i[1:])
                    elif i[0] == '4':
                        result.append("3" + i[1:])
                    elif i[0] == '5':
                        result.append("4" + i[1:])
                if num == '3':  # GDT_helmet
                    if i[0] == None:
                        result.append(None)
                    # if i[1].isdigit():
                    #     continue
                    if i[0] == '4':  # wear helmet
                        result.append("1" + i[1:])
                    if i[0] == '5':  # no helmet
                        result.append("0" + i[1:])
                    if i[0] == '1' and i[1] == '4':  #骑摩托车
                        result.append("1" + i[2:])
                    if i[0] == '1' and i[1] == '5':  #保安
                        result.append("0" + i[2:])
                    if i[0] == '1' and i[1] == '6':  #帽子
                        result.append("0" + i[2:])
                    if i[0] == '1' and i[1] == '7':  #改造
                        result.append("0" + i[2:])
                if num == '4':  # helmet
                    if i[0] == None:
                        result.append(None)
                    if i[0] == '0':
                        result.append("1" + i[1:])
                    if i[0] == '1':
                        result.append("0" + i[1:])
                if num == '5':  # GDT_fire
                    if i[0] == None:
                        result.append(None)
                    if i[1].isdigit():
                        continue
                    if i[0] == '6':
                        result.append("0" + i[1:])
                if num == '6':  # GDT_glitter
                    if i[0] == None:
                        result.append(None)
                    if i[0] == '9':
                        result.append("0" + i[1:])
                    if i[0] == '1' and i[1] == '0':
                        result.append("1" + i[2:])
                    if i[0] == '1' and i[1] == '3':  # 不规范
                        result.append("0" + i[2:])
                    if i[1].isdigit():
                        continue
                if num == '7':  # GDT_glitter_new
                    if i[0] == None:
                        result.append(None)
                    if i[0] == '9':
                        result.append("0" + i[1:])
                    if i[0] == '1' and i[1] == '0':
                        result.append("1" + i[2:])
                    if i[0] == '1' and i[1] == '3':  # 不规范
                        result.append("2" + i[2:])
                    if i[1].isdigit():
                        continue
                if num == '8':  # Helmet_Glitter   helmet
                    if i[0] == None:
                        result.append(None)
                    if i[0] == '0':
                        result.append("0" + i[1:])
                    elif i[0] == '1':
                        result.append("1" + i[1:])
                if num == '9':  # Helmet_Glitter   glitter
                    if i[0] == None:
                        result.append(None)
                    if i[0] == '2':  # no wear
                        result.append("1" + i[1:])
                    elif i[0] == '3':
                        result.append("0" + i[1:])
                if num == '10':  # GDT_truck
                    if i[0] == None:
                        result.append(None)
                    if i[0] == '3':
                        result.append("0" + i[1:])
                    # elif i[1].isdigit():
                    #     continue
                    elif i[0] == '1' and i[1] == '4':
                        result.append("1" + i[2:])
                    elif i[0] == '1' and i[1] == '5':
                        result.append("2" + i[2:])
                    elif i[0] == '1' and i[1] == '6':
                        result.append("3" + i[2:])
                if num == '10':  # GDT_truck
                    if i[0] == None:
                        result.append(None)
                    if i[0] == '3':
                        result.append("0" + i[1:])
                    # elif i[1].isdigit():
                    #     continue
                    elif i[0] == '1' and i[1] == '4':
                        result.append("1" + i[2:])
                    elif i[0] == '1' and i[1] == '5':
                        result.append("2" + i[2:])
                    elif i[0] == '1' and i[1] == '6':
                        result.append("3" + i[2:])
                if num == '11':  # GDT_glitter
                    if i[0] == None:
                        result.append(None)
                    if i[0] == '6':
                        result.append("0" + i[1:])
                    if i[0] == '7':
                        result.append("1" + i[2:])
                    if i[0] == '8':  # 不规范
                        result.append("0" + i[2:])
            with open(txt_path, "w") as f:
                f.writelines(result)
    # sleep(0.2)
    print('转换完成')


def draw(num, path, ori_img, save_path):
    # path = input('input label path(../labels):')                  #"/media/vs/Data/darknet_train_result/Truck0406/labels2"  #label address
    # path1 = input('input images path(../images):')                # "/media/vs/Data/darknet_train_result/Truck0406/Truck0406"  #pictures address
    # path2 = input('input drawed iamges path(../val_images):')      #"/media/vs/Data/darknet_train_result/Truck0406/test"   #drawed pictures address

    path = path + '/labels'
    path1 = ori_img
    # path1 = ori_img + '/images'
    path2 = save_path + '/val'
    if not os.path.exists(path2):
        os.makedirs(path2)
    for root, dirs, files in os.walk(path):
        # n = int(len(files)*0.2)
        # result = random.sample(files, 10)
        for name in tqdm(files):
            if name.endswith(".txt"):
                filename = root + "/" + name  # /media/wst/Data/darknet训练结果/darknet训练结果/TruckCover/darknet_275_closetransportation/train/labels/31801994.txt
                file_name = name.split('.')[0]  # name = 31801994.txt      file_name = 31801994
                file_path = path1 + "/" + file_name + ".jpg"  # label对应的图片
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
                    if num == '1':  # GDT_TRUCK
                        if cls == '1':  # close
                            cv2.rectangle(img, c1, c2, (128, 0, 0), 2)
                            img = puttext(img, '密闭', (c1), (128, 0, 0), 20, 'yuyang.ttf', "BL")
                        if cls == '2':  # OPEN
                            cv2.rectangle(img, c1, c2, (0, 128, 160), 2)
                            img = puttext(img, '打开', (c1), (0, 128, 160), 20, 'yuyang.ttf', "BL")
                        if cls == '3':  # Incomplete close
                            cv2.rectangle(img, c1, c2, (192, 192, 64), 2)
                            img = puttext(img, '未覆盖完全', (c1), (192, 192, 64), 20, 'yuyang.ttf', "BL")
                        if cls == '4':  # OTHERS
                            cv2.rectangle(img, c1, c2, (0, 128, 64), 2)
                            img = puttext(img, '其他类车', (c1), (0, 128, 64), 20, 'yuyang.ttf', "BL")
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
                            img = puttext(img, '未覆盖完全', (c1), (192, 192, 64), 20, 'yuyang.ttf', "BL")
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
                    if num == '9':  # CLT
                        if cls == '1':
                            cv2.rectangle(img, c1, c2, (0, 0, 128), 2)
                            img = puttext(img, '车身_货车', (c1), (0, 0, 128), 20, 'yuyang.ttf', "BL")
                        if cls == '2':
                            cv2.rectangle(img, c1, c2, (0, 128, 192), 2)
                            img = puttext(img, '车身_泵车', (c1), (0, 128, 192), 20, 'yuyang.ttf', "BL")
                        if cls == '3':
                            cv2.rectangle(img, c1, c2, (128, 64, 128), 2)
                            img = puttext(img, '车身_挖掘机', (c1), (128, 64, 128), 20, 'yuyang.ttf', "BL")
                        if cls == '4':
                            cv2.rectangle(img, c1, c2, (128, 192, 128), 2)
                            img = puttext(img, '车身_土方车', (c1), (128, 192, 128), 20, 'yuyang.ttf', "BL")
                        if cls == '5':
                            cv2.rectangle(img, c1, c2, (64, 0, 192), 2)
                            img = puttext(img, '车身_面包车', (c1), (64, 0, 192), 20, 'yuyang.ttf', "BL")
                        if cls == '6':
                            cv2.rectangle(img, c1, c2, (64, 192, 128), 2)
                            img = puttext(img, '车身_洒水车', (c1), (64, 192, 128), 20, 'yuyang.ttf', "BL")
                        if cls == '7':
                            cv2.rectangle(img, c1, c2, (192, 64, 192), 2)
                            img = puttext(img, '车身_拖拉机', (c1), (192, 64, 192), 20, 'yuyang.ttf', "BL")
                        if cls == '8':
                            cv2.rectangle(img, c1, c2, (128, 128, 160), 2)
                            img = puttext(img, '车身_三轮摩托车', (c1), (128, 128, 160), 20, 'yuyang.ttf', "BL")
                        if cls == '9':
                            cv2.rectangle(img, c1, c2, (0, 64, 160), 2)
                            img = puttext(img, '车身_摩托车', (c1), (0, 64, 160), 20, 'yuyang.ttf', "BL")
                        if cls == '10':
                            cv2.rectangle(img, c1, c2, (0, 192, 224), 2)
                            img = puttext(img, '车身_搅拌机', (c1), (0, 192, 224), 20, 'yuyang.ttf', "BL")
                        if cls == '11':
                            cv2.rectangle(img, c1, c2, (192, 0, 160), 2)
                            img = puttext(img, '车身_轿车', (c1), (192, 0, 160), 20, 'yuyang.ttf', "BL")
                        if cls == '12':
                            cv2.rectangle(img, c1, c2, (192, 192, 0), 2)
                            img = puttext(img, '货车车斗_有货', (c1), (192, 192, 0), 20, 'yuyang.ttf', "BL")
                        if cls == '13':
                            cv2.rectangle(img, c1, c2, (64, 64, 64), 2)
                            img = puttext(img, '货车车斗_无货', (c1), (64, 64, 64), 20, 'yuyang.ttf', "BL")
                        if cls == '14':
                            cv2.rectangle(img, c1, c2, (0, 160, 0), 2)
                            img = puttext(img, '货车车斗_厢子', (c1), (0, 160, 0), 20, 'yuyang.ttf', "BL")
                        if cls == '15':
                            cv2.rectangle(img, c1, c2, (128, 32, 0), 2)
                            img = puttext(img, '土方车车斗_闭', (c1), (128, 32, 0), 20, 'yuyang.ttf', "BL")
                        if cls == '16':
                            cv2.rectangle(img, c1, c2, (128, 96, 64), 2)
                            img = puttext(img, '土方车车斗_开', (c1), (128, 96, 64), 20, 'yuyang.ttf', "BL")
                        if cls == '17':
                            cv2.rectangle(img, c1, c2, (192, 160, 224), 2)
                            img = puttext(img, '土方车车斗_未完全闭', (c1), (192, 160, 224), 20, 'yuyang.ttf', "BL")
                        if cls == '18':
                            cv2.rectangle(img, c1, c2, (128, 96, 128), 2)
                            img = puttext(img, '车牌_绿牌', (c1), (128, 96, 128), 20, 'yuyang.ttf', "BL")
                        if cls == '19':
                            cv2.rectangle(img, c1, c2, (0, 224, 224), 2)
                            img = puttext(img, '车牌_黄牌', (c1), (0, 224, 224), 20, 'yuyang.ttf', "BL")
                        if cls == '20':
                            cv2.rectangle(img, c1, c2, (192, 64, 64), 2)
                            img = puttext(img, '车牌_蓝牌', (c1), (192, 64, 64), 20, 'yuyang.ttf', "BL")
                        if cls == '21':
                            cv2.rectangle(img, c1, c2, (192, 224, 32), 2)
                            img = puttext(img, '车牌_其他', (c1), (192, 224, 32), 20, 'yuyang.ttf', "BL")
                        if cls == '22':
                            cv2.rectangle(img, c1, c2, (192, 224, 32), 2)
                            img = puttext(img, '车头', (c1), (192, 224, 32), 20, 'yuyang.ttf', "BL")
                        if cls == '23':
                            cv2.rectangle(img, c1, c2, (64, 160, 224), 2)
                            img = puttext(img, '洒水车_洒水', (c1), (64, 160, 224), 20, 'yuyang.ttf', "BL")
                        if cls == '24':
                            cv2.rectangle(img, c1, c2, (192, 160, 128), 2)
                            img = puttext(img, '洒水车_未洒水', (c1), (192, 160, 128), 20, 'yuyang.ttf', "BL")
                        if cls == '25':
                            cv2.rectangle(img, c1, c2, (192, 192, 192), 2)
                            img = puttext(img, '车牌_车身车辆', (c1), (192, 192, 192), 20, 'yuyang.ttf', "BL")
                        if cls == '26':
                            cv2.rectangle(img, c1, c2, (0, 0, 32), 2)
                            img = puttext(img, '冲洗区域', (c1), (0, 0, 32), 20, 'yuyang.ttf', "BL")
                        if cls == '27':
                            cv2.rectangle(img, c1, c2, (64, 192, 192), 2)
                            img = puttext(img, '大门', (c1), (64, 192, 192), 20, 'yuyang.ttf', "BL")
                        if cls == '28':
                            cv2.rectangle(img, c1, c2, (255, 144, 24), 2)
                            img = puttext(img, '车身_拖车', (c1), (255, 144, 24), 20, 'yuyang.ttf', "BL")
                        if cls == '29':
                            cv2.rectangle(img, c1, c2, (128, 0, 64), 2)
                            img = puttext(img, '车身_吊车', (c1), (128, 0, 64), 20, 'yuyang.ttf', "BL")
                        if cls == '30':
                            cv2.rectangle(img, c1, c2, (192, 160, 64), 2)
                            img = puttext(img, '过水池', (c1), (192, 160, 64), 20, 'yuyang.ttf', "BL")
                    if num == '10':  # 广联达CLT
                        if cls == '0':  # wear
                            cv2.rectangle(img, c1, c2, (0, 0, 192), 2)
                            img = puttext(img, '土方车', (c1), (0, 0, 192), 20, 'yuyang.ttf', "BL")
                        if cls == '1':  # wear
                            cv2.rectangle(img, c1, c2, (0, 0, 192), 2)
                            img = puttext(img, '土方车车斗_闭', (c1), (0, 0, 192), 20, 'yuyang.ttf', "BL")
                        if cls == '2':  # wear
                            cv2.rectangle(img, c1, c2, (0, 0, 192), 2)
                            img = puttext(img, '土方车车斗_开', (c1), (0, 0, 192), 20, 'yuyang.ttf', "BL")
                        if cls == '3':  # wear
                            cv2.rectangle(img, c1, c2, (0, 0, 192), 2)
                            img = puttext(img, '土方车车斗_未完全闭', (c1), (0, 0, 192), 20, 'yuyang.ttf', "BL")
                    if num == '11':  # helmet
                        if cls == '0':  # no
                            cv2.rectangle(img, c1, c2, (0, 0, 192), 2)
                            img = puttext(img, '人', (c1), (0, 0, 192), 20, 'yuyang.ttf', "BL")
                        if cls == '1':  # no
                            cv2.rectangle(img, c1, c2, (0, 0, 192), 2)
                            img = puttext(img, '人', (c1), (0, 0, 192), 20, 'yuyang.ttf', "BL")


                cv2.imwrite(path2 + "/" + file_name + ".jpg", img)
                f.close()
    sleep(0.2)
    print('绘制图片完成')


if __name__ == '__main__':
    mp.set_start_method('spawn')
    main()
