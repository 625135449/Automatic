import os
import cv2
import xml.etree.ElementTree as ET
def double_label(dir,input_labels,path):
    # input_labels = r'/media/vs/Data/darknet_train_result/darknet/Helmet/helmet_top/PR/all_test/labels/'#原始darknet标签的路径
    # output_labels = r'/media/vs/Data/darknet_train_result/darknet/Helmet/helmet_top/PR/all_test/GT/'#转换之后的路径
    # dir='/media/vs/Data/darknet_train_result/darknet/Helmet/helmet_top/PR/all_test/images/'#原始图片的路径
    output_labels = path + '/GT/'
    if not os.path.exists(output_labels):
        os.makedirs(output_labels)
    def bbox2points(bbox):
        """
        From bounding box yolo format
        to corner points cv2 rectangle
        """
        x, y, w, h = bbox
        xmin = float((float(x) - (float(w) / 2)))
        xmax = float((float(x) + (float(w) / 2)))
        ymin = float((float(y) - (float(h) / 2)))
        ymax = float((float(y) + (float(h) / 2)))
        return xmin, ymin, xmax, ymax


    for txt_name in os.listdir(input_labels):
        w = cv2.imread(dir + txt_name.strip('txt') + 'jpg')
        print(txt_name)
        a=w.shape
        height=a[0]
        height=float(height)
        width=a[1]
        width=float(width)
        # print(height,width)

        txt_path = input_labels + txt_name
        with open(txt_path, 'r') as f1:
            lines = f1.readlines()
        # print(lines)
        list1 = []
        l1 = []
        for i in lines:
            l = i.strip('\n').split(' ')  # 将每一行的数据加入列表
            num = 0
            for j in l:
                if num<5:
                    if num %2== 0 and num!=0:
                        j=float(j)
                        j = j*height
                        l1.append(j)
                        num += 1
                    elif num%2==1:
                        j=float(j)
                        j=j*width
                        l1.append(j)
                        num += 1
                    else:
                        l1.append(j)
                        num += 1
        # print(l1)
        for i in range(0,len(l1),5):
            # print(l1[i:i+5])
            xmina=bbox2points(l1[i+1:i+5])
            xmina=list(xmina)
            xmina.insert(0,l1[i+0])
            list1.append(xmina)
        # print(list1)

        with open(output_labels + txt_name , 'w') as f2:
            for i in range(len(list1)):
                num = 0
                for j in list1[i]:
                    # print(j)
                    j = str(j)
                    f2.write(j + ' ')
                    num += 1
                    if num % 5==0:
                        f2.write("\n")

