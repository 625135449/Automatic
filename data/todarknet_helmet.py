import json
import os
from time import sleep
from tqdm import tqdm


def helmet_reverse(j_path, path):
    # json_path = input(
    #     'input json_report path(../example.json_report):')  # '/media/vs/Data/darknet_train_result/Truck0406/Truck0406.json_report'
    # label_path = input(
    #     'input labels saved path(../labels/):')  # '/media/vs/Data/darknet_train_result/Truck0406/labels2/'
    # train_path = os.path.join(
    #     label_path + '/' + 'train.txt')  # r'/media/vs/Data/darknet_train_result/Truck0406/labels2/train.txt'  # 转换成的train保存路径
    json_path = j_path
    label_path = path + '/' + 'labels' + '/'
    train_path = os.path.join(label_path + 'train.txt')
    f = open(json_path, encoding='utf-8')
    content = json.load(f)
    folder = os.path.join(label_path)
    if not os.path.exists(folder):
        os.makedirs(folder)
    file2 = open(train_path, 'a')
    # for _ in tqdm(range(1)):
    img_len = len(content['images'])
    for i in tqdm(range(img_len)):
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
                    # if content['images'][i]['label'][k]['category_id'] != 0:
                    if content['images'][i]['label'][k]['coordinate_type'] == "RECTANGLE":
                        xleft = content['images'][i]['label'][k]['coordinate'][0]  # 获取左上角x的位置比例
                        yleft = content['images'][i]['label'][k]['coordinate'][1]  # 获取左上角y的位置比例

                        x = content['images'][i]['label'][k]['coordinate'][2]  # x与宽的比例
                        y = content['images'][i]['label'][k]['coordinate'][3]  # Y与高的比例

                        if x >= 0.009 and y >= 0.01:

                            y2 = y + (y * 0.05)  # 高扩大5%
                            x2 = x + (x * 0.05)

                            x0left = (xleft - (x * 0.05)) * width
                            y0left = (yleft - (y * 0.05)) * height

                            x3 = (xleft + x + (x * 0.1)) * width
                            y3 = (yleft + y + (y * 0.1)) * height

                            x1 = xleft + ((1 / 2) * x)
                            y1 = yleft + (1 / 2) * y
                            # 获取中心点的比例
                            try:
                                if x0left < 0 and y0left > 0:
                                    x1, y1, x, y = x1, y1, x, y + (y * 0.1)  # 宽加大5%，高加大10%

                                if x0left < 0 and y0left < 0:
                                    x1, y1, x, y = x1, y1, x, y

                                if x0left > 0 and y0left > 0:
                                    x1, y1, x, y = x1, y1, x + (x * 0.1), y + (y * 0.1)  # 宽加大10%，高加大10%

                                if x0left > 0 and y0left < 0:
                                    x1, y1, x, y = x1, y1, x + (x * 0.1), y  # 宽加大10%，高加大5%

                                if x3 > width and y3 < height:
                                    x1, y1, x, y = x1, y1, x, y + (y * 0.1)  # 宽加大5%，高加大10%

                                if x3 > width and y3 > height:
                                    x1, y1, x, y = x1, y1, x, y

                                if x3 < width and y3 > height:
                                    x1, y1, x, y = x1, y1, x + (x * 0.1), y  # 宽加大10%，高加大10%

                                if x3 < width and y3 < height:
                                    x1, y1, x, y = x1, y1, x + (x * 0.1), y + (y * 0.1)  # 宽加大10%，高加大5%
                                else:
                                    x1 = xleft + ((1 / 2) * x)
                                    y1 = yleft + (1 / 2) * y
                                x1 = '%.6f' % x1
                                y1 = '%.6f' % y1
                                x = '%.6f' % x
                                y = '%.6f' % y
                                for j in range(l_len):
                                    id = content['label_category'][j]['id']
                                    if content['images'][i]['label'][k]['category_id'] == id:
                                        name = str(j) + ' ' + x1 + ' ' + y1 + ' ' + x + ' ' + y + '\n'
                                        file3.write(name)
                            except TypeError:
                                continue
                        else:
                            continue
            else:
                _ = ''
                file3.write(_)
                file3.close()
        except TypeError:
            _ = ''
            file3.write(_)
            file3.close()
    file2.close()
    os.remove(train_path)
    sleep(0.2)
    print('制作标签完成')
