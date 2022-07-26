import os
from os.path import join
import multiprocessing as mp
from data.shuffle import make_test
from data.todarknet_helmet import json_reverse
from data.todarknet_json import truck_reverse
from data.draw_pic import draw_label


# json_path = r'/media/vs/Data/darknet_train_result/Truck0406/Truck0406.json_report'
# train_path = r'/media/vs/Data/darknet_train_result/Truck0406/labels2/train.txt'  # 转换成的train保存路径
img_bg = None


def input_window(img, msg, color='blue'):
    print(msg)
    return input('>')


def main():
    # project_name = input_window(img_bg,'Input project name to create a new project, \nor [ENTER] directly to select a existed project:')
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

        selected_operation = 0
        while selected_operation >= 0:
            print('----Operations----')
            print('[1] check file')
            print('[2] Reverse json_report')
            print('[3] Reverse json_report (helmet)')
            print('[4] Draw label')
            print('[5] Train the model')
            print('[6] Recheck labels')
            print('[7] make test data')
            print('[0] Exit')
            selected_operation = int(input_window(img_bg, 'What do you want to do?'))
            project_name = project_list[selected_project_index - 1]
            select_path = join('project', project_name)
            if selected_operation == 0:
                return
            if selected_operation == 1:
                check_project(select_path)
            if selected_operation == 2:
                truck_reverse()
            if selected_operation == 3:
                path = ''
                json_path = ''
                json_reverse()
            if selected_operation == 4:
                draw_label()
            if selected_operation == 5:
                train()
            if selected_operation == 6:
                num = input('1:GDT_truck 2:close_transportation 3:GDT_helmet 4:helmet 5:GDT_fire 6:GDT_glitter (selecte the num):')
                path = input('labels address(../labels/):')
                recheck_truckcover(path, num)
            if selected_operation == 7:
                path = select_path
                imgpath = ''
                make_test(path,imgpath)
    else:
        if os.path.exists(join('.', 'project', project_name)) is True:
            print('The proposed project name is existed. Bye.')
            return
        # create_new_project(project_name)

def check_project(select_path):
    print('当前路径:',select_path)       #project/test
    file_list = os.listdir(select_path)          #读取所有文件
    project_list = []
    for p in file_list:
        project_list.append(p)

    if len(file_list)==0 :
        print('nothing. Bye.')
        return
    else:
        print('当前文件夹下的所有的文件数量(%d):' % len(file_list))
        project_list.sort()
        for i, p in enumerate(project_list):
            if os.path.isdir(join(select_path, p)):
                file_list2 = os.listdir(join(select_path,p))
                print('[%d] %s (%d)' % (i + 1, p,len(file_list2)))
            else:
                print('[%d] %s' % (i + 1, p))

    selected_project_index = -1
    while not (0 < selected_project_index <= len(project_list)):
        selected_project_index = int(input_window(img_bg, 'Select one project'))

    selected_operation = 0

    while selected_operation >= 0:
        print('----Operations----')
        print('[1] check file')
        print('[2] Reverse json_report')
        print('[3] Reverse json_report (helmet)')
        print('[4] Draw label')
        print('[5] Train the model')
        print('[6] Recheck labels')
        print('[7] make test data')
        print('[0] Exit')
        selected_operation = int(input_window(img_bg, 'What do you want to do?'))
        project_name = project_list[selected_project_index - 1]
        path = join(select_path,project_name)
        if selected_operation == 0:
            return
        if selected_operation == 1:
            check_project(path)
        if selected_operation == 2:
            truck_reverse()
        if selected_operation == 3:
            json_reverse()
        if selected_operation == 4:
            draw_label()
        if selected_operation == 5:
            train()
        if selected_operation == 6:
            num = input('1:GDT_truck 2:close_transportation 3:GDT_helmet 4:helmet 5:GDT_fire 6:GDT_glitter (selecte the num):')
            path = input('labels address(../labels/):')
            recheck_truckcover(path,num)
        if selected_operation == 7:
            path = select_path
            imgpath = ''
            make_test(path, imgpath)

def train():
    os.system("cd ~/darknet && find `pwd`/train -name \*.jpg > train.list && ./darknet detector train build/darknet/x64/data/obj.data cfg/yolo-obj.cfg build/darknet/x64/yolov4.conv.137")


def recheck_truckcover(path,num):
    for _, _, files in os.walk(path):
        for f in files:
            txt_path = os.path.join(path, f)
            with open(txt_path, "r") as f:
                lines = f.readlines()
            result = []
            for i in lines:
                if num == '1':         #GDT_truck
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

                if num == '2':                #truck
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

                if num =='3':        #GDT_helmet
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
    print('转换完成')

if __name__ == '__main__':
    mp.set_start_method('spawn')
    main()
