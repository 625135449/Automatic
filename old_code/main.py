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
            while not (0 < selected_project_index1 <= len(project_list)):
                selected_project_index1 = int(input_window(img_bg, 'Select one project'))
            selected_operation1 = 0
            while selected_operation1 >= 0:
                print('----Operations----')
                print('[1] check file')
                print('[2] Reverse json_report')
                print('[3] Reverse json_report (helmet)')
                print('[4] Recheck labels')
                print('[5] Enhance data')
                print('[6] Enhance data(lift)')
                print('[7] Train the model')
                print('[8] Draw label')
                print('[9] make test data')
                print('[0] Exit')
                selected_operation = int(input_window(img_bg, 'What do you want to do?'))
                project_name2 = project_list1[selected_project_index1 - 1]  # pro/test/test.json_report
                select_path2 = join(select_path, project_name2)
                select = join(select_path, project_list1[0])  # iamges 第一个
                fileList = os.listdir(select_path)  # 读取所有文件
                #save function
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
                        '1:GDT_truck 2:close_transportation 3:GDT_helmet 4:helmet 5:GDT_fire 6:GDT_glitter (selecte the num):')
                    path = select_path + '/labels/'
                    recheck_truckcover(path, num)
                if selected_operation == 5:
                    img_path = select + '/'
                    labels_p = labels_path + '/'
                    save_p = save_path + '/'
                    enhance(img_path, labels_p, save_p)
                if selected_operation == 6:
                    # labels_path = select_path + '/labels'
                    # save_path = select_path + '/save'
                    arg(select, labels_path, save_path)
                if selected_operation == 7:
                    train()
                if selected_operation == 8:
                    num = input(
                        '1:GDT_truck 2:close_transportation 3:helmet 4:fire 5:glitter 6:mask (selecte the num):')
                    # draw_label(num, select, select_path)
                    draw_label(num, save_path, save_path)
                if selected_operation == 9:
                    path = select_path
                    make_test(path, select)




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
                    if i[1].isdigit():
                        continue
                    if i[0] == '4':  # wear helmet
                        result.append("1" + i[1:])
                    if i[0] == '5':  # no helmet
                        result.append("0" + i[1:])
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
                    if i[1].isdigit():
                        continue
            with open(txt_path, "w") as f:
                f.writelines(result)
    # sleep(0.2)
    print('转换完成')


if __name__ == '__main__':
    mp.set_start_method('spawn')
    main()
