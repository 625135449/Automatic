import os
import numpy as np
import matplotlib.pyplot as plt
import time
from multiprocessing import Lock, Process, Queue, current_process, Pool, Manager

task_result = Queue()

# 除了iou阈值和文件位置，其他的都不用改
##########################
# 文件计数，计算每个类别对应的recall的分母，返回一个列表
def count1(dir, output_labels):
    recall_fenmu = []

    with open(dir, 'r') as f:
        f = f.readlines()
        c = len(f)

    for i in range(c):
        print(str(i))
        recall_cat_fenmu = cal_tp_fn(output_labels, str(i))  # 计算recall的分母，订值
        recall_fenmu.append(recall_cat_fenmu)

    return recall_fenmu, f


# 计算recall的分母元素,GT
def cal_tp_fn(dir, category):
    # print("Dir: ", dir)

    count = 0

    for txt_name in os.listdir(dir):
        txt_path = os.path.join(dir, txt_name)
        # txt_path = dir + txt_name
        with open(txt_path, 'r') as f1:
            lines = f1.readlines()
        for i in lines:
            l = i.strip('\n').split(' ')  # 将每一行的数据加入列表
            if category in l:
                count += 1

    return count


def readDT(dir, catid):
    l = []
    txt_path = []

    with open(catid, 'r') as f:
        name = f.readlines()

    for i, v in enumerate(name): name[i] = '_' + v

    for txt_name in os.listdir(dir):
        l.append(txt_name)

    for i in range(len(name)):
        for j in range(len(l)):
            if name[i].strip('\n') in str(l[j]):
                txt_path.append(os.path.join(dir, l[j]))
                # txt_path.append(dir + l[j])
    return txt_path


def cal_pre_fenmu1(l):
    precisiom_fenmu_final = []

    for i in l:
        pre_fenmu = precisiom_fenmu2(i)
        precisiom_fenmu_final.append(pre_fenmu)

    return precisiom_fenmu_final


def precisiom_fenmu2(txt):
    # print(txt)
    precisiom_fenmu = []

    for i in range(0, 100, 5):
        pr_fenmu = cal_tp_fp(txt, float(i / 100.0))  # 计算precision的分母，变值
        if pr_fenmu != 0:
            precisiom_fenmu.append(pr_fenmu)

    return precisiom_fenmu


# 计算precision的分母,DT
def cal_tp_fp(dir, threshod1):
    count = 0
    with open(dir, 'r') as f1:
        lines = f1.readlines()
        for i in lines:
            l = i.strip('\n').split(' ')
            if len(l) > 0 and float(l[1]) > threshod1:
                count += 1

    return count


# 固定bbox1,变换bbox2
def iou(bbox1, bbox2, center=False):
    """Compute the iou of two boxes.
    Parameters
    ----------
    bbox1, bbox2: list.
        The bounding box coordinates: [xmin, ymin, xmax, ymax] or [xcenter, ycenter, w, h].
    center: str, default is 'False'.
        The format of coordinate.
        center=False: [xmin, ymin, xmax, ymax]
        center=True: [xcenter, ycenter, w, h]
    Returns
    -------
    iou: float.
        The iou of bbox1 and bbox2.
    """
    if center == False:
        xmin1, ymin1, xmax1, ymax1 = bbox1
        xmin2, ymin2, xmax2, ymax2 = bbox2
        xmin1 = int(float(xmin1))
        ymin1 = int(float(ymin1))
        xmin2 = int(float(xmin2))
        ymin2 = int(float(ymin2))
        xmax2 = int(float(xmax2))
        xmax1 = int(float(xmax1))
        ymax1 = int(float(ymax1))
        ymax2 = int(float(ymax2))

    else:
        xmin1, ymin1 = int(float(bbox1[0]) - float(bbox1[2]) / 2.0), int(float(bbox1[1]) - float(bbox1[3]) / 2.0)
        xmax1, ymax1 = int(float(bbox1[0]) + float(bbox1[2]) / 2.0), int(float(bbox1[1]) + float(bbox1[3]) / 2.0)
        xmin2, ymin2 = int(float(bbox2[0]) - float(bbox2[2]) / 2.0), int(float(bbox2[1]) - float(bbox2[3]) / 2.0)
        xmax2, ymax2 = int(float(bbox2[0]) + float(bbox2[2]) / 2.0), int(float(bbox2[1]) + float(bbox2[3]) / 2.0)

    # 获取矩形框交集对应的顶点坐标(intersection)
    xx1 = np.max([xmin1, xmin2])
    yy1 = np.max([ymin1, ymin2])
    xx2 = np.min([xmax1, xmax2])
    yy2 = np.min([ymax1, ymax2])

    # 计算两个矩形框面积
    area1 = (xmax1 - xmin1 ) * (ymax1 - ymin1 )
    area2 = (xmax2 - xmin2 ) * (ymax2 - ymin2 )

    # 计算交集面积
    inter_area = (np.max([0, xx2 - xx1])) * (np.max([0, yy2 - yy1]))
    # 计算交并比
    iou = inter_area / (area1 + area2 - inter_area + 1e-6)

    return iou


# ======读取类别

def cat_id(k, catid):
    with open(catid, 'r') as f:
        name = f.readlines()
    for i, v in enumerate(name): name[i] = '_' + v
    # print('name', name)
    for n in range(len(name)):
        if name[n].strip('\n') in str(k):
            catid = str(n)
        else:
            pass
    return k, catid


def count(x):
    c = 0
    # print(x)
    for i in x:
        if i != None and float(i) > 0:
            c += 1
    return c


def job1(input):
    out, txt_name, l, o = input
    # print(f"start process {txt_name}")
    a = []
    for i in range(0, 100, 5):
        x = com2(out, txt_name, l, float(i / 100.0), o)  # x是大于指定阈值下计算得到的iou最大的iou
        c = count(x)
        if c != 0:
            a.append(c)
    task_result.put(a)
    # print(f"end process {txt_name}")


# 计算分子
# out = GT path，涉及到逻辑cpu的个数
def com1(out, l, o):
    result = []
    p = Pool(6)
    payload = []
    for txt_name in os.listdir(out):
        params = [out, txt_name, l, o]
        payload.append(params)
    p.map(job1, payload)
    task_result.put('Done')
    while True:
        a = task_result.get()
        if len(a) > 0 and a != 'Done':
            result.append(a)
        if a == 'Done':
            break
    return result


def com2(out, txt_name, l, thresh1, o):
    a = []
    filename = os.path.join(out, txt_name)
    with open(filename, 'r') as f:
        f = f.readlines()
        for i in f:
            l2 = []
            l1 = i.strip('\n').strip(' ').split(' ')
            if str(o) in l1:
                for j in l1:
                    l2.append(j)
            if len(l2) > 0:
                x = com3(l2, txt_name, l, thresh1)
                a.append(x)
    return a


# 0.6的iou阈值,该函数控制iou的阈值
def com3(l1, txt_name, l, thresh1):
    aa = []
    with open(l, 'r') as f1:
        line3 = f1.readlines()
    for i in line3:
        l3 = i.strip('\n').split(' ')
        if l3[0] == txt_name.strip('.').strip('txt').strip('.') and float(l3[1]) > thresh1:
            a = iou(l1[1:5], l3[2:6], False)
            if float(a) > 0.65:
                aa.append(a)
    if len(aa) > 0:
        x = sorted(aa, reverse=True)[0]
        return x


# 每个类别每个阈值下必须有值，没有的添加0，目前是20个阈值
def add_thresh_number(list1):
    for i in range(0, len(list1)):
        for j in range(len(list1[i]), 20):
            list1[i].append(0)
    a = np.array(list1)
    sum1 = np.sum(a, axis=0)
    return sum1


# 存储最终结果
def list2txt_finalrecall(list2):
    with open("final_recall.txt", "w") as output:
        count = 0
        for i in list2:
            output.write(str(i))
            output.write(' ')
            count += 1
            if count == 20:
                output.write('\n')


def list2txt_finalprecision(list2):
    with open('final_precision.txt', 'w') as f:
        for i in range(len(list2)):
            for j in list2[i]:
                f.write(str(j))
                f.write(' ')
            f.write('\n')
    return True


# 计算recall的分子/分母
def cal_recal_result(result_fenzi, recall_fenmu):
    final_recall = []
    for m in range(len(result_fenzi)):
        a = [float(i) / recall_fenmu[m] for i in result_fenzi[m]]
        final_recall.append(a)

    return final_recall


# 计算precision的分子/分母
def cal_precision_result(result_fenzi, precision_fenmu):
    final_precision = []
    for j in range(len(result_fenzi)):
        y1 = list(map(lambda x: float(x[0]) / float(x[1]), zip(result_fenzi[j], precision_fenmu[j])))
        if len(y1) != len(result_fenzi[j]):
            for nu in range(len(result_fenzi[j]) - len(y1)):
                y1.append(0)
        final_precision.append(y1)

    return final_precision


def draw_curve(recall_list, precision_list, catid_name_list):
    catid_name_list.append('average')
    allcolornames = ['k', 'g', 'b', 'r', 'y', 'c', 'm', 'olive', 'purple', 'hotpink', 'dodgerblue', 'darksage',
                     'midnightblue', 'forestgreen', 'darkorange', 'lightseagreen', 'darkgoldenrod', 'darkslategray',
                     'plum', 'crimson',
                     'dimgray', 'maroon', 'tomato', 'sienna', 'lawngreen', 'steelblue', 'orchid', 'burlywood',
                     'slategrey', 'royalblue']
    x_final = [sum(e) / len(e) for e in zip(*recall_list)]
    y_final = [sum(e) / len(e) for e in zip(*precision_list)]
    recall_list.append(x_final)
    precision_list.append(y_final)
    for i in range(len(recall_list)):
        n = len(recall_list[i])
        print(n)
        txt = []
        plt.plot(recall_list[i], precision_list[i], color=allcolornames[i], linewidth=1, alpha=0.6,
                    label=catid_name_list[i])
        for k in range(0, 100, 5):
            txt.append(str(k / 100.0))
        for j in range(n):
            plt.annotate(txt[j], (recall_list[i][j], precision_list[i][j]))
    plt.legend()
    plt.xlabel('recall')
    plt.ylabel('precision')
    plt.title('P-R curve')
    plt.savefig(fname='result.svg',dpi=600)
    plt.show()


def main1(output_labels,mask_name,DT):
    # recall的分母,第一个数字是0，代表没有带安全帽

    recall_fenmu, c = count1(mask_name, output_labels)
    print('every category recall_fenmu:', recall_fenmu)
    category = []
    for i in c:
        i = i.strip('\n')
        category.append(i)
    print('cat', category)

    # precision的分母,每个阈值下的个数，输出三中类别的个数
    pr_fenmu = readDT(DT, mask_name)
    print("pr_fenmu: ", pr_fenmu)
    pre_final = cal_pre_fenmu1(pr_fenmu)
    print('every category precision_fenmu:', pre_final)

    # 计算分子
    result_fenzi = []
    for i in pr_fenmu:
        # print(i)
        l, o = cat_id(i,mask_name)
        print(l, o)
        x = com1(output_labels, l, o)
        if x:
            numb = add_thresh_number(x)
            print('fenzi', numb)
            result_fenzi.append(numb)
    print(result_fenzi)
    # 画图求每个类别的recall保存到final_recall.txt,一个列表
    # 分母计算是按类别0，1，2计算的，
    final_recall = cal_recal_result(result_fenzi, recall_fenmu)

    list2txt_finalrecall(final_recall)
    print('final_recall:', final_recall)
    # 画图求每个类别的precision的结果保存到final_precision.txt,一个大列表中每类放在一个列表
    # 分子和分母的顺序一样
    final_precision = cal_precision_result(result_fenzi, pre_final)
    list2txt_finalprecision(final_precision)
    print('final_precision:', final_precision)
    # 画P-r曲线
    # ======每个类别得曲线
    draw_curve(final_recall, final_precision, category)


