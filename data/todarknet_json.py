import json
import os
from tqdm import tqdm
from time import sleep

def json_reverse(pic_len,j_path,path):
    # json_path = input('input json_report path(../example.json_report):')                       #'/media/vs/Data/darknet_train_result/Truck0406/Truck0406.json_report'
    # label_path = input('input labels saved path(../labels/):')                       #'/media/vs/Data/darknet_train_result/Truck0406/labels2/'
    # train_path = os.path.join(label_path + '/' + 'train.txt')                        # r'/media/vs/Data/darknet_train_result/Truck0406/labels2/train.txt'  # 转换成的train保存路径

    json_path = j_path
    label_path = path + '/' +'labels/'
    train_path = os.path.join(label_path + '/' + 'train.txt')

    if os.path.exists(train_path):
        os.remove(train_path)
    f = open(json_path, encoding='utf-8')
    content = json.load(f)

    folder = os.path.join(label_path)
    if not os.path.exists(folder):
        os.makedirs(folder)

    file2 = open(train_path, 'a')
    i_len = len(content['images'])
    for i in tqdm(range(i_len)):
        width = (content['images'][i]['width'])  # 读取图片的宽
        height = (content['images'][i]['height'])  # 读取图片的长
        img_name = content['images'][i]["filename"]
        (img_name, extension) = os.path.splitext(img_name)
        file_name = img_name
        json_name = os.path.join(folder + file_name + '.txt')
        file3 = open(json_name, 'a')
        try:
            i_l_len = len(content['images'][i]['label'])
            l_len = len(content['label_category'])
            if i_l_len != 0:
                for k in range(i_l_len):
                    if content['images'][i]['label'][k]['coordinate_type'] == "RECTANGLE":
                        xleft = content['images'][i]['label'][k]['coordinate'][0]  # 获取左上角x的位置比例 x/宽
                        yleft = content['images'][i]['label'][k]['coordinate'][1]  # 获取左上角y的位置比例 y/高
                        x = content['images'][i]['label'][k]['coordinate'][2]  # 矩形宽与宽的比例
                        y = content['images'][i]['label'][k]['coordinate'][3]  # 矩形高与高的比例
                        try:
                            x1 = ((width * xleft) + (1 / 2) * (x * width)) / width
                            y1 = ((height * yleft) + (1 / 2) * (y * height)) / height
                        except TypeError:
                            continue
                        x1 = '%.6f' % x1
                        y1 = '%.6f' % y1
                        x = '%.6f' % x
                        y = '%.6f' % y

                        for j in range(l_len):
                            id = content['label_category'][j]['id']
                            if content['images'][i]['label'][k]['category_id'] == id:
                                name = str(j) + ' ' + x1 + ' ' + y1 + ' ' + x + ' ' + y + '\n'
                                file3.write(name)
                    elif content['images'][i]['label'][k]['coordinate_type'] == "POLYGON":
                        x = sorted(content['images'][i]['label'][k]['coordinate'], key=lambda x: x[0])
                        y = sorted(content['images'][i]['label'][k]['coordinate'], key=lambda x: x[1])
                        xmin, ymin, xmax, ymax = x[0][0], y[0][1], x[-1][0], y[-1][1]
                        x2 = xmax - xmin
                        y2 = ymax - ymin
                        # 获取中心点的比例
                        try:
                            x1 = ((width * xmin) + (1 / 2) * (x2 * width)) / width
                            y1 = ((height * ymin) + (1 / 2) * (y2 * height)) / height
                        except TypeError as e:
                            print(e)
                            continue
                        x1 = '%.6f' % x1
                        y1 = '%.6f' % y1
                        x = '%.6f' % x2
                        y = '%.6f' % y2

                        for j in range(l_len):
                            id = content['label_category'][j]['id']
                            if content['images'][i]['label'][k]['category_id'] == id:
                                name = str(j) + ' ' + x1 + ' ' + y1 + ' ' + x + ' ' + y + '\n'
                                file3.write(name)
            else:
                k=''
                file3.write(k)
                file3.close()
        except TypeError:
            k = ''
            file3.write(k)
            file3.close()
    file2.close()
    os.remove(train_path)
    print('制作标签完成')
