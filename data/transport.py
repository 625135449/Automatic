from PIL import Image
import uuid
import os

def trans(name,img_path,save_img, label_path,save_lb):
    # PicPath = "/media/vs/Data/aist/project/test/labels_ori/0a0c6b51-5436-4993-852a-aebb183b7d48.jpg"
    # out = img.transpose(Image.FLIP_LEFT_RIGHT)     #水平翻转
    # out = img.rotate(45)                          #45°顺时针翻转
    # newname = "/media/vs/Data/aist/project/test/images/0a0c6b51-5436-4993-852a-aebb183b7d48.jpg"
    img = Image.open(img_path)
    out = img.transpose(Image.FLIP_TOP_BOTTOM)    #垂直翻转,二维数组的transpose操作就是对原数组的转置操作
    uuid1 = uuid.uuid4()
    # img_new = str(uuid1) + '.jpg'
    img_new = 'trans' + name[:-4] + '.jpg'
    newname = os.path.join(save_img,img_new)
    out.save(newname)
    # image = Image.open('/media/vs/Data/aist/project/test/images/0a0c6b51-5436-4993-852a-aebb183b7d48.jpg')
    image = Image.open(newname)
    image = image.convert('RGB')
    w, h = image.size
    txt_path = label_path + '/'+ name[:-4] + '.txt'
    txt_save = save_lb + '/' + img_new[:-4] + '.txt'
    with open(txt_path, "r") as f:
        lines = f.readlines()
    result = []
    for j in lines:
        i = j.split(" ")
        y_center =( h - (float(i[2]) * h ) )/ h
        y0= '%.6f' % y_center
        result.append(i[0]+' '+i[1]+' ' + y0 +' '+ i[3] +' '+i[4])
    with open(txt_save, "w") as f:
        f.writelines(result)
    # print('转换完成')

