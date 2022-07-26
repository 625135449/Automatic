import json
import os
from tqdm import tqdm


def get_message(label_path, content, content_len):
    width = (content['images'][content_len]['width'])  # 读取图片的宽
    height = (content['images'][content_len]['height'])  # 读取图片的长
    img_name = content['images'][content_len]["filename"]
    images_name = os.path.splitext(img_name)[0]
    json_name = os.path.join(label_path, '{}.{}'.format(images_name, 'txt'))
    return width, height, json_name


def get_coordinate(content, content_len, label_len):
    x_left = content['images'][content_len]['label'][label_len]['coordinate'][0]  # 获取左上角x的位置比例
    y_left = content['images'][content_len]['label'][label_len]['coordinate'][1]  # 获取左上角y的位置比例
    x = content['images'][content_len]['label'][label_len]['coordinate'][2]  # x与宽的比例
    y = content['images'][content_len]['label'][label_len]['coordinate'][3]  # Y与高的比例
    return x_left, y_left, x, y


def classes_dict(json_path):
    """

        返回一个字典：{'id': name}

    """
    class_dict = {}
    with open(json_path, 'r', encoding='utf-8') as f:
        content = json.load(f)
    l_len = len(content['label_category'])
    for category_len in range(l_len):
        dict_key = content['label_category'][category_len]['id']
        class_dict[dict_key] = content['label_category'][category_len]['name']
    return class_dict


def fgh_reverse(json_path, save_to):
    fgh_class = ["guard", "improper wear glitter", "no glitter", "wear glitter"]
    category_dict = classes_dict(json_path)
    label_none = ''  # 写入空标签
    category_map_dict = {}  # 存储json获取的类别对应一个序号，传给映射方案

    label_path = os.path.join(save_to, 'labels')
    os.makedirs(label_path, exist_ok=True)
    with open(json_path, 'r') as f:
        content = json.load(f)

    for content_len in tqdm(range(len(content['images']))):
        width, height, json_name = get_message(label_path, content, content_len)
        with open(json_name, 'a') as final_file:
            images_label_len = len(content['images'][content_len]['label'])
            label_category_len = len(content['label_category'])

            if images_label_len != 0:
                for label_len in range(images_label_len):
                    if content['images'][content_len]['label'][label_len]['coordinate_type'] == "RECTANGLE":
                        x_left, y_left, x, y = get_coordinate(content, content_len, label_len)

                        if x >= 0.009 and y >= 0.01:  # 16x16
                            present_id = content['images'][content_len]['label'][label_len]['category_id']
                            present_name = category_dict[present_id]

                            if present_name in fgh_class:  # 判断是帽子一类：安全帽、摩托车头盔......
                                try:
                                    x1 = ((width * x_left) + (1 / 2) * (x * width)) / width
                                    y1 = ((height * y_left) + (1 / 2) * (y * height)) / height
                                except TypeError:
                                    continue
                                x1, y1, x, y = '%.6f' % x1, '%.6f' % y1, '%.6f' % x, '%.6f' % y

                                for category_len in range(label_category_len):
                                    category_id = content['label_category'][category_len]['id']
                                    # 保存例如，{'Helmet':0,'Glitter':1}
                                    category_map_dict[
                                        content['label_category'][category_len]['name']] = category_len
                                    if content['images'][content_len]['label'][label_len]['category_id'] == \
                                            category_id:
                                        name = f"{str(category_len)}{' '}{x1}{' '}{y1}{' '}{x}{' '}{y}\n"
                                        final_file.write(name)
                            else:
                                x0left, y0left = (x_left - (x * 0.05)) * width, (y_left - (y * 0.05)) * height
                                x3, y3 = (x_left + x + (x * 0.1)) * width, (y_left + y + (y * 0.1)) * height
                                x1, y1 = x_left + ((1 / 2) * x), y_left + (1 / 2) * y
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
                                        x1 = x_left + ((1 / 2) * x)
                                        y1 = y_left + (1 / 2) * y
                                    x1, y1, x, y = '%.6f' % x1, '%.6f' % y1, '%.6f' % x, '%.6f' % y

                                    for category_len in range(label_category_len):
                                        category_id = content['label_category'][category_len]['id']
                                        # 保存例如，{'Helmet':0,'Glitter':1}
                                        category_map_dict[
                                            content['label_category'][category_len]['name']] = category_len
                                        if content['images'][content_len]['label'][label_len]['category_id'] == \
                                                category_id:
                                            name = f"{str(category_len)}{' '}{x1}{' '}{y1}{' '}{x}{' '}{y}\n"
                                            final_file.write(name)

                                except TypeError:
                                    continue
                        else:
                            continue
            else:
                final_file.write(label_none)
