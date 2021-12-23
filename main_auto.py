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
import shutil
import time

img_bg = None

########配置环境#####################
nfs_path_qi = '/mnt/shared/qi'
nfs_path_qing = '/mnt/shared/qing'
nfs_path_hou = '/mnt/shared/hou'
###################################


def input_window(img, msg, color='blue'):
    print(msg)
    return input('>')


nfs_path1 = nfs_path_qi + '/Helmet'
nfs_path2 = nfs_path_qing + '/Glitter'
nfs_path3 = nfs_path_hou + '/CLT'


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
            select_path = join('project', project_name)  # project/helmet0715
            project_list1 = []
            select_p = {}
            print('当前路径:', select_path)  # project/test

            for r, d, f in os.walk(select_path):
                for i in d:
                    if os.path.isdir(join(r, i)):
                        img_path = join(r, i)
                        os.rename(img_path, join(r, 'images'))  # project/test/images

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
                    for i in file_list2:
                        if '.jpg' in i or 'jpeg' in i or '.png' in i:
                            select_img_path = join(select_path, p)  # imgpath
                            select_p['img'] = select_img_path
                        break
                else:
                    json_path = join(select_path, p)
                    select_p['json_report'] = json_path
                    print('[%d] %s' % (i + 1, p))

            selected_project_index1 = -1
            flag = 0

            selected_operation1 = 0
            while selected_operation1 >= 0:
                # print('----------方案选择列表----------')
                print('********数据增强方案选择*********')
                print('[1] 安全帽(GDT)')
                print('[2] 安全帽(Lift)')
                print('[3] 安全帽(带标签上传)')
                print('[4] 反光衣(2个类)')
                print('[5] 反光衣(3个类)')
                print('[6] 反光衣(带标签上传)')
                print('[7] CLT34')
                # print()
                print('********原始数据方案选择**********')
                print('[8] 安全帽(GDT)')
                print('[9] 安全帽(Lift)')
                print('[10] 安全帽(带标签上传)')
                print('[11] 反光衣(2个类)')
                print('[12] 反光衣(3个类)')
                print('[13] 反光衣(带标签上传)')
                print('[14] CLT34')
                selected_operation = int(input_window(img_bg, '请选择方案序号'))

                # project_name2 = project_list1[selected_project_index1 - 1]  # pro/test/test.json_report
                project_name2 = project_list1[1]  # json_report
                # select_path2 = join(select_path, project_name2)
                # select = join(select_path, project_list1[0])  # images 第一个
                select_path2 = select_p['json_report']
                select = select_p['img']
                fileList = os.listdir(select_path)  # 读取所有文件
                file_time = data_time()  # 获取当天时间
                # save function
                labels_path = select_path + '/labels'
                save_path = select_path + '/save'
                pic = []
                for p in fileList:
                    pic.append(p)
                pic_len = len(pic)
                # if selected_operation == 0:
                #     return
                if selected_operation == 1:  # helmet
                    helmet_reverse(select_path2, select_path)  # labels
                    path = select_path + '/labels/'
                    recheck_truckcover(path, '3')  # 映射
                    img_path, labels_p, save_p = select + '/', labels_path + '/', save_path + '/'
                    enhance(img_path, labels_p, save_p)  # 数据增强
                    ori_img = save_path + '/images'
                    draw_label('3', save_path, ori_img, save_path)  # 绘图
                    save_img = save_path + '/images'
                    make_test(save_path, save_img)  # 测试集
                    new_file = 'Helmet_' + file_time  # Helmet_20210805
                    # nfs_path = nfs_path_qi + '/helmet'
                    # shutil.copytree('/media/vs/Data/aist/project/20210805', os.path.join(nfs_path,new_file))   #改文件夹名字，拷贝到nfs
                    print('开始拷贝训练数据')
                    shutil.move(select_path, os.path.join(nfs_path1, new_file))
                    print('拷贝完成')
                    return

                if selected_operation == 2:  # helmet
                    helmet_reverse(select_path2, select_path)  # labels
                    path = select_path + '/labels/'
                    # recheck_truckcover(path, '3')          #映射
                    img_path, labels_p, save_p = select + '/', labels_path + '/', save_path + '/'
                    enhance(img_path, labels_p, save_p)  # 数据增强
                    ori_img = save_path + '/images'
                    draw_label('3', save_path, ori_img, save_path)  # 绘图
                    save_img = save_path + '/images'
                    make_test(save_path, save_img)  # 测试集
                    new_file = 'Helmet_' + file_time  # Helmet_20210805
                    # nfs_path = nfs_path_qi + '/helmet'
                    # shutil.copytree('/media/vs/Data/aist/project/20210805', os.path.join(nfs_path,new_file))   #改文件夹名字，拷贝到nfs
                    print('开始拷贝训练数据')
                    shutil.move(select_path, os.path.join(nfs_path1, new_file))
                    print('拷贝完成')
                    return

                if selected_operation == 3:  # Helmet_Glitter   helmet   带标签上传
                    json_reverse(pic_len, select_path2, select_path)  # labels  不放大
                    path = select_path + '/labels/'
                    recheck_truckcover(path, '8')  # 映射
                    img_path, labels_p, save_p = select + '/', labels_path + '/', save_path + '/'
                    enhance(img_path, labels_p, save_p)  # 数据增强
                    ori_img = save_path + '/images'
                    draw_label('3', save_path, ori_img, save_path)  # 绘图
                    save_img = save_path + '/images'
                    make_test(save_path, save_img)  # 测试集
                    new_file = 'Helmet_' + file_time  # Helmet_20210805
                    print('开始拷贝训练数据')
                    shutil.move(select_path, os.path.join(nfs_path1, new_file))
                    print('拷贝完成')
                    return

                if selected_operation == 4:  # glitter---2class
                    json_reverse(pic_len, select_path2, select_path)  # labels
                    path = select_path + '/labels/'
                    recheck_truckcover(path, '6')  # 映射
                    img_path, labels_p, save_p = select + '/', labels_path + '/', save_path + '/'
                    enhance(img_path, labels_p, save_p)  # 数据增强
                    ori_img = save_path + '/images'
                    draw_label('5', save_path, ori_img, save_path)  # 绘图
                    save_img = save_path + '/images'
                    make_test(save_path, save_img)  # 测试集
                    new_file2 = 'Glitter_' + file_time
                    print('开始拷贝训练数据')
                    shutil.move(select_path, os.path.join(nfs_path2, new_file2))  # 改文件夹名字，拷贝到nfs
                    print('拷贝完成')
                    return

                if selected_operation == 5:  # glitter---3class
                    json_reverse(pic_len, select_path2, select_path)  # labels
                    path = select_path + '/labels/'
                    recheck_truckcover(path, '7')  # 映射
                    img_path, labels_p, save_p = select + '/', labels_path + '/', save_path + '/'
                    enhance(img_path, labels_p, save_p)  # 数据增强
                    ori_img = save_path + '/images'
                    draw_label('5', save_path, ori_img, save_path)  # 绘图
                    save_img = save_path + '/images'
                    make_test(save_path, save_img)  # 测试集
                    new_file3 = 'Glitter_' + file_time
                    print('开始拷贝训练数据')
                    shutil.move(select_path, os.path.join(nfs_path2, new_file3))  # 改文件夹名字，拷贝到nfs
                    print('拷贝完成')
                    return

                if selected_operation == 6:  # Helmet_Glitter   glitter
                    json_reverse(pic_len, select_path2, select_path)  # labels
                    path = select_path + '/labels/'
                    recheck_truckcover(path, '9')  # 映射
                    img_path, labels_p, save_p = select + '/', labels_path + '/', save_path + '/'
                    enhance(img_path, labels_p, save_p)  # 数据增强
                    ori_img = save_path + '/images'
                    draw_label('5', save_path, ori_img, save_path)  # 绘图
                    save_img = save_path + '/images'
                    make_test(save_path, save_img)  # 测试集
                    new_file3 = 'Glitter_' + file_time
                    print('开始拷贝训练数据')
                    shutil.move(select_path, os.path.join(nfs_path2, new_file3))  # 改文件夹名字，拷贝到nfs
                    print('拷贝完成')
                    return

                if selected_operation == 7:  # CLT34
                    json_reverse(pic_len, select_path2, select_path)  # labels
                    path = select_path + '/labels/'
                    # recheck_truckcover(path, '1')  # 映射
                    img_path, labels_p, save_p = select + '/', labels_path + '/', save_path + '/'
                    enhance(img_path, labels_p, save_p)  # 数据增强
                    ori_img = save_path + '/images'
                    draw_label('1', save_path, ori_img, save_path)  # 绘图
                    save_img = save_path + '/images'
                    make_test(save_path, save_img)  # 测试集
                    new_file3 = 'CLT34_' + file_time
                    print('开始拷贝训练数据')
                    shutil.move(select_path, os.path.join(nfs_path3, new_file3))  # 改文件夹名字，拷贝到nfs
                    print('拷贝完成')
                    return

                ###################################################################################
                if selected_operation == 8:  # helmet
                    helmet_reverse(select_path2, select_path)  # labels
                    path = select_path + '/labels/'
                    recheck_truckcover(path, '3')  # 映射
                    draw_label('3', select_path, select, select_path)  # ori_img,save_ori 绘图
                    make_test(select_path, select)  # 测试集
                    new_file = 'Helmet_' + file_time
                    print('开始拷贝训练数据')
                    shutil.move(select_path, os.path.join(nfs_path1, new_file))  # 改文件夹名字，拷贝到nfs
                    print('拷贝完成')
                    return

                if selected_operation == 9:  # helmet
                    helmet_reverse(select_path2, select_path)  # labels
                    path = select_path + '/labels/'
                    # recheck_truckcover(path, '3')          #映射
                    draw_label('3', select_path, select, select_path)  # ori_img,save_ori 绘图
                    make_test(select_path, select)  # 测试集
                    new_file = 'Helmet_' + file_time
                    print('开始拷贝训练数据')
                    shutil.move(select_path, os.path.join(nfs_path1, new_file))  # 改文件夹名字，拷贝到nfs
                    print('拷贝完成')
                    return

                if selected_operation == 10:  # helmet
                    json_reverse(pic_len, select_path2, select_path)  # labels
                    path = select_path + '/labels/'
                    recheck_truckcover(path, '8')  # 映射
                    draw_label('3', select_path, select, select_path)  # ori_img,save_ori 绘图
                    make_test(select_path, select)  # 测试集
                    new_file = 'Helmet_' + file_time
                    print('开始拷贝训练数据')
                    shutil.move(select_path, os.path.join(nfs_path1, new_file))  # 改文件夹名字，拷贝到nfs
                    print('拷贝完成')
                    return

                if selected_operation == 11:  # glitter---2class
                    json_reverse(pic_len, select_path2, select_path)  # labels
                    path = select_path + '/labels/'
                    recheck_truckcover(path, '6')  # 映射
                    draw_label('5', select_path, select, select_path)  # ori_img,save_ori 绘图
                    make_test(select_path, select)  # 测试集
                    new_file3 = 'Glitter_' + file_time
                    print('开始拷贝训练数据')
                    shutil.move(select_path, os.path.join(nfs_path2, new_file3))  # 改文件夹名字，拷贝到nfs
                    print('拷贝完成')
                    return

                if selected_operation == 12:  # glitter---3class
                    json_reverse(pic_len, select_path2, select_path)  # labels
                    path = select_path + '/labels/'
                    recheck_truckcover(path, '7')  # 映射
                    draw_label('5', select_path, select, select_path)  # ori_img,save_ori 绘图
                    make_test(select_path, select)  # 测试集
                    new_file3 = 'Glitter_' + file_time
                    print('开始拷贝训练数据')
                    shutil.move(select_path, os.path.join(nfs_path2, new_file3))  # 改文件夹名字，拷贝到nfs
                    print('拷贝完成')
                    return

                if selected_operation == 13:  # Helmet_Glitter   glitter
                    json_reverse(pic_len, select_path2, select_path)  # labels
                    path = select_path + '/labels/'
                    recheck_truckcover(path, '9')  # 映射
                    draw_label('5', select_path, select, select_path)  # ori_img,save_ori 绘图
                    make_test(select_path, select)  # 测试集
                    new_file3 = 'Glitter_' + file_time
                    print('开始拷贝训练数据')
                    shutil.move(select_path, os.path.join(nfs_path2, new_file3))  # 改文件夹名字，拷贝到nfs
                    print('拷贝完成')
                    return

                if selected_operation == 14:  # truck
                    json_reverse(pic_len, select_path2, select_path)  # labels
                    path = select_path + '/labels/'
                    # recheck_truckcover(path, '1')  # 映射
                    draw_label('1', select_path, select, select_path)  # ori_img,save_ori 绘图
                    make_test(select_path, select)  # 测试集
                    new_file3 = 'CLT34_' + file_time
                    print('开始拷贝训练数据')
                    shutil.move(select_path, os.path.join(nfs_path3, new_file3))  # 改文件夹名字，拷贝到nfs
                    print('拷贝完成')
                    return


def data_time():
    NowTime = time.localtime()  # 获取当前时间
    a = time.strftime("%Y%m%d", NowTime)
    return a


def train():
    os.system(
        "cd ~/darknet && find `pwd`/train -name \*.jpg > train.list && ./darknet detector train build/darknet/x64/data/obj.data cfg/yolo-obj.cfg build/darknet/x64/yolov4.conv.137")


def recheck_truckcover(path, num):
    for _, _, files in os.walk(path):
        for f in tqdm(files):
            txt_path = os.path.join(path, f)
            with open(txt_path, "r") as f:
                lines = f.readlines()
            result = []
            for i in lines:
                # if num == '1':  # GDT_truck
                #     if i[0] == None:
                #         result.append(None)
                #     if i[0] == '0':
                #         result.append("2" + i[1:])
                #     elif i[1].isdigit():
                #         continue
                #     elif i[0] == '1':
                #         result.append("1" + i[1:])
                #     elif i[0] == '2':
                #         result.append("3" + i[1:])
                #     elif i[0] == '3':
                #         result.append("4" + i[1:])
                if num == '1':  # CLT33
                    if i[0] == None:
                        result.append(None)
                    if i[0] == '0':
                        result.append("0" + i[1:])
                    if i[0] == '3' and i[1] == '4':  #工程车
                        continue
                    elif i[1].isdigit():
                        result.append("0" + i[1:])
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
                    if i[1].isdigit():
                        continue
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
            with open(txt_path, "w") as f:
                f.writelines(result)

        # sleep(0.2)
        print('标签映射完成')


if __name__ == '__main__':
    mp.set_start_method('spawn')
    main()
