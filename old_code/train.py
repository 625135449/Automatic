import os
from os.path import join, splitext, exists
import cv2 as cv
from models import *
import json_report
from tqdm import tqdm
from multiprocessing.pool import Pool
from multiprocessing import cpu_count
import multiprocessing as mp
import random
import time
import json_report

json_path = r'/media/vs/Data/darknet_train_result/Truck0406/Truck0406.json'
train_path = r'/media/vs/Data/darknet_train_result/Truck0406/labels2/train.txt'   #转换成的train保存路径
img_bg = None

def input_window(img, msg, color='blue'):
    print(msg)
    return input('>')

def main():
    project_name = input_window(img_bg, 'Input project name to create a new project, \nor [ENTER] directly to select a existed project:')
    if project_name == '':
        file_list = os.listdir('project')
        project_list = []
        for p in file_list:
            if os.path.isdir(join('project', p)):

                project_list.append(p)

        if len(project_list) == 0:
            print('No project is existed. Bye.')
            return

        print('List all the project (%d):' % len(project_list))
        project_list.sort()
        for i, p in enumerate(project_list):
            print('[%d] %s' % (i + 1, p))

        selected_project_index = -1
        while not (0 < selected_project_index <= len(project_list)):
            selected_project_index = int(input_window(img_bg, 'Select one project'))

        selected_operation = 0

        while selected_operation >= 0:
            print('----Operations----')
            print('[1] Check project')
            print('[2] Check, and make raw data to training data')
            print('[3] Train the model')
            print('[4] Check, make data and train')
            print('[0] Exit')
            selected_operation = int(input_window(img_bg, 'What do you want to do?'))
            project_name = project_list[selected_project_index - 1]
            if selected_operation == 0:
                return
            if selected_operation == 1:
                check_project(project_name)
            if selected_operation == 2:
                samples, settings, max_step = check_project(project_list[selected_project_index - 1])
                if settings['VERSION'].lower() in ['v3', 'v3t', 'v4', 'v4t']:
                    make_detection_data(project_name, samples, settings)

                if settings['VERSION'].lower() in ['d9', 'd19']:
                    make_classification_data(project_name, samples, settings)

            if selected_operation == 3:
                samples, settings, max_step = check_project(project_list[selected_project_index - 1])
                train(project_list[selected_project_index - 1], settings, max_step)

    else:
        if os.path.exists(join('.', 'project', project_name)) is True:
            print('The proposed project name is existed. Bye.')
            return
        create_new_project(project_name)


if __name__ == '__main__':
    mp.set_start_method('spawn')
    main()
