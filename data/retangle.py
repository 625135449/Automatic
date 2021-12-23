from PIL import Image
import os


def pic_rec(name, img_uuid, img_path, save_path, label_path,save_lb):
    # path = '/home/fei/Desktop/test'
    # save_path ='/home/fei/Desktop/save'
    # if not os.path.exists(save_path):
    #     os.mkdir(save_path)
    # for root, dirs, files in os.walk(path):
    #     for name in files:
    # if name.endswith(".jpg"):
    # img_path = root +'/' + name
    image = Image.open(img_path)
    image = image.convert('RGB')
    w, h = image.size
    background = Image.new('RGB', size=(max(w, h), max(w, h)), color=(0, 0, 0))  # 创建背景图，颜色值为127
    length = int(abs(w - h) // 2)  # 一侧需要填充的长度
    box = (length, 0) if w < h else (0, length)  # 粘贴的位置
    background.paste(image, box)  # 背景图.past(前景图，位置（左上角，右下角）)
    # image_data =background.resize((768, 768))
    # background.save(save_path + '/' + img_uuid)
    background.save(save_path + '/' + 'ret' + name)
    txt_path = label_path + '/'+ name[:-4] + '.txt'
    # txt_save = save_lb + '/' + img_uuid[:-4] + '.txt'
    txt_save = save_lb + '/' + 'ret' + name[:-4] + '.txt'
    with open(txt_path, "r") as f:
        lines = f.readlines()
    result = []
    for j in lines:
        i = j.split(" ")
        if w > h:
            y_center = (float(i[2]) * h + length) / w
            y_h = (float(i[4]) * h) / w
            y0, y = '%.6f' % y_center, '%.6f' % y_h
            result.append(i[0]+' '+i[1]+' ' + y0 +' '+ i[3] +' '+ y + '\n')
        if w < h:
            x_center = (float(i[1]) * w + length) / h
            x_h = (float(i[3]) * w) / h
            x0, x = '%.6f' % x_center, '%.6f' % x_h
            result.append(i[0]+' '+x0+' ' + i[2] +' '+ x +' '+ i[4])   #文本自含/n
    with open(txt_save, "w") as f:
        f.writelines(result)
    # print('转换完成')
# cv2.imwrite(path + "/" + "3.jpg", image_data)
# background.show()
# image_data.show()
