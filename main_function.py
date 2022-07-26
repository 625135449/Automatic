from os.path import join
import multiprocessing as mp
from data.shuffle import make_test
from data.todarknet_helmet import helmet_reverse
from data.todarknet_json import json_reverse
from data.fgh_reverse import fgh_reverse
from data.draw import draw_label
from data.enhance import enhance
from data.data_arg import arg
import os
from tqdm import tqdm

img_bg = None


def input_window(msg):
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
            selected_project_index = int(input_window('Select one project'))

            project_name = project_list[selected_project_index - 1]
            select_path = join('project', project_name)
            project_list1 = []
            print('当前路径:', select_path)  # project/test

            for r, d, f in os.walk(select_path):
                for i in d:
                    if os.path.isdir(join(r, i)):
                        ori_img_path = join(r, i)
                        if not os.path.exists(join(r, 'images')):
                            os.rename(ori_img_path, join(r, 'images'))
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
            flag = 0  # 初始状态
            while not (0 < selected_project_index1 <= len(project_list)):
                selected_project_index1 = int(input_window('Select one project'))
            selected_operation1 = 0
            while selected_operation1 >= 0:
                print('--------功能菜单--------')
                print('[1] 检查文件数量')
                print('[2] 制作labels')
                print('[3] 制作labels(FGH)')
                print('[4] 制作labels(helmet)')
                print('[5] 标签映射')
                print('[6] 数据增强')
                print('[7] 数据增强(电梯)')
                print('[8] 制作测试集')
                print('[9] 绘制图片')
                print('[0] 退出')
                selected_operation = int(input_window('What do you want to do?'))
                project_name2 = project_list1[selected_project_index1 - 1]  # pro/test/test.json_report
                select_path2 = join(select_path, project_name2)
                select = join(select_path, 'images')
                file_list = os.listdir(select_path)  # 读取所有文件

                # save function
                labels_path = f"{select_path}{'/labels'}"
                save_path = f"{select_path}{'/save'}"
                pic = []
                for p in file_list:
                    pic.append(p)
                pic_len = len(pic)
                if selected_operation == 0:
                    return
                if selected_operation == 1:
                    check_project(select_path)
                if selected_operation == 2:
                    json_reverse(pic_len, select_path2, select_path)
                if selected_operation == 3:
                    fgh_reverse(select_path2, select_path)
                if selected_operation == 4:
                    helmet_reverse(select_path2, select_path)
                if selected_operation == 5:
                    num = input('1:GDT_truck 2:close_transportation 3:GDT_helmet 4:helmet 5:GDT_fire 6:GDT_glitter '
                                '7:GDT_improper_glitter 8:Helmet_Glitter(Helmet) 9:CLT(30类） '
                                '10:CLT_TO_GLD 11：FGH(反光衣)')
                    path = f"{select_path}{'/labels/'}"
                    recheck_truck_cover(path, num)
                if selected_operation == 6:
                    img_path = f"{select}{'/'}"
                    labels_p = f"{labels_path}{'/'}"
                    save_p = f"{save_path}{'/'}"
                    enhance(img_path, labels_p, save_p)
                    flag = 1  # 增强
                if selected_operation == 7:
                    arg(select, labels_path, save_path)
                    # salt(select_path,save_img,save_lb)
                    flag = 1
                if selected_operation == 8:
                    if flag >= 1:
                        save_img = save_path + '/images'
                        make_test(save_path, save_img)
                    else:
                        make_test(select_path, select)
                if selected_operation == 9:
                    option = input('1：绘制全部图片 2：随机绘制十张图片:')
                    num = input('1:CLT(34) 2:GLD 3:helmet 4:fire 5:glitter 6:mask '
                                '7:improper glitter 8:Helmet_Glitter(helmet and glitter) 9:MSC 10：FGH '
                                '13:GLD_VSD 14:GLD_GDD：')
                    if flag == 1 and option == '2':  # 绘制增强的10张图片
                        ori_img = f"{save_path}{'/images'}"
                        draw_label(num, save_path, ori_img, save_path)
                        flag = 1

                    elif flag == 1 and option == '1':  # 绘制增强的全部图片
                        ori_img = f"{save_path}{'/images'}"
                        draw_label(num, save_path, ori_img, save_path)
                        flag = 1

                    elif flag == 0 and option == '2':  # 绘制未增强的10张图片
                        draw_label(num, select_path, select, select_path)
                        flag = 0
                    else:  # 绘制未增强的全部图片
                        draw_label(num, select_path, select, select_path)  # ori_img,save_ori
                        flag = 0


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
        selected_project_index1 = int(input_window('Select one project'))
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


def recheck_truck_cover(path, num):
    for _, _, files in os.walk(path):
        for f in tqdm(files):
            txt_path = os.path.join(path, f)
            with open(txt_path, "r") as file:
                lines = file.readlines()
            result = []
            for i in lines:
                if num == '1':  # GDT_truck
                    if i[0] is None:
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
                    if i[0] is None:
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
                    if i[0] is None:
                        result.append(None)
                    # if i[1].isdigit():
                    #     continue
                    if i[0] == '4':  # wear helmet
                        result.append("1" + i[1:])
                    if i[0] == '5':  # no helmet
                        result.append("0" + i[1:])
                    if i[0] == '1' and i[1] == '4':  # 骑摩托车
                        result.append("1" + i[2:])
                    if i[0] == '1' and i[1] == '5':  # 保安
                        result.append("0" + i[2:])
                    if i[0] == '1' and i[1] == '6':  # 帽子
                        result.append("0" + i[2:])
                    if i[0] == '1' and i[1] == '7':  # 改造
                        result.append("0" + i[2:])
                if num == '4':  # helmet
                    if i[0] is None:
                        result.append(None)
                    if i[0] == '0':
                        result.append("1" + i[1:])
                    if i[0] == '1':
                        result.append("0" + i[1:])
                if num == '5':  # GDT_fire
                    if i[0] is None:
                        result.append(None)
                    if i[1].isdigit():
                        continue
                    if i[0] == '6':
                        result.append("0" + i[1:])
                if num == '6':  # GDT_glitter
                    if i[0] is None:
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
                    if i[0] is None:
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
                    if i[0] is None:
                        result.append(None)
                    if i[0] == '0':
                        result.append("0" + i[1:])
                    elif i[0] == '1':
                        result.append("1" + i[1:])
                if num == '9':  # Helmet_Glitter   glitter
                    if i[0] is None:
                        result.append(None)
                    if i[0] == '2':  # no wear
                        result.append("1" + i[1:])
                    elif i[0] == '3':
                        result.append("0" + i[1:])
                if num == '10':  # CLT_TO_GLD
                    if i[0] is None:
                        result.append(None)
                    if i[0] == '3':  # 土方车
                        if i[1].isdigit():
                            continue
                        else:
                            result.append("0" + i[1:])
                    elif i[0] == '1' and i[1] == '4':  # 土方车车斗_闭
                        result.append("1" + i[2:])
                    elif i[0] == '1' and i[1] == '5':  # 土方车车斗_开
                        result.append("2" + i[2:])
                    elif i[0] == '1' and i[1] == '6':  # 土方车车斗_未完全开
                        result.append("3" + i[2:])
                    elif i[0] == '3' and i[1] == '2':  # 土方车车斗_顶棚破损
                        result.append("2" + i[2:])
                if num == '11':  # GDT_glitter
                    if i[0] is None:
                        result.append(None)
                    if i[0] == '6':
                        result.append("0" + i[1:])
                    if i[0] == '7':
                        result.append("1" + i[2:])
                    if i[0] == '8':  # 不规范
                        result.append("0" + i[2:])
            with open(txt_path, "w") as file_r:
                file_r.writelines(result)
    # sleep(0.2)
    print('转换完成')


if __name__ == '__main__':
    mp.set_start_method('spawn')
    main()
