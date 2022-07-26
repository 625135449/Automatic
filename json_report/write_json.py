import json
import os
from os.path import join
from tqdm import tqdm


path = '/media/vs/Data/aist/json_report/20210715'
save_json = '/media/vs/Data/aist/json_report/json_result'          #生成的json地址
test_path = '/media/vs/Data/aist/json_report/test'                 #test集的label

if not os.path.exists(save_json):
    os.makedirs(save_json)

report_dict = {'map': [7600],'label_count':[],'PR_img':[]}
map_re = {}
path_dict = {}
model_path = {}
label_count = {}

def get_path():
    for r,d,files in os.walk(path):
        for i in files:
            _i = i.split('.')[0]
            i_ = i.split('.')[1]
            if _i == 'data':
                d = join(path, i)  # /home/fei/darknet/Helmet/model/data.txt
                model_path['data'] = d
            if _i == 'name':
                d = join(path, i)  # /home/fei/darknet/Helmet/model/data.txt
                model_path['name'] = d
            if i_ == 'cfg':
                c = join(path, i)
                model_path['cfg'] = c
            if i_ == 'weights' or i_ == 'conv':
                w = join(path, i)
                model_path['weights'] = w

def map(data,cfg,weights,path):
    log = path + '/map.logs'
    os.system("cd ~/darknet &&./darknet detector map %s %s %s 2>&1 |tee %s"%(data,cfg,weights,log))

def get_map(log):
    result = []
    re = []
    r = []
    with open(log, 'r') as f:  #'/media/vs/Data/aist/project/20210805/save/map.logs'
        lines = f.readlines()
        for line in lines:
            if 'class_id' in line:
                result.append(line)
    for i in result:
        j = i.split(',')
        re.append(j)
    for i in re:
        for j in i:
            k = j.strip()   #去除空格
            r.append(k)
    for i in r:
        if 'name' in i :
            map_re[i] = r[r.index(i) + 1].split('  ')[0]   #{'name = no helmet': 'ap = 87.24%', 'name = wear helmet': 'ap = 94.42%'}


def count_label(test,name):
    # name = '/media/vs/新加卷/Qing/G0805/model/Glitter.name'  # 类别txt地址
    # result_path = '/media/vs/新加卷/Qing/G0805/test_result'  # 存放的result地址
    label_path = test + '/labels'
    result_path = test + '/result'

    key = []
    value = []
    i = 0
    with open(name, "r") as f:
        lines = f.readlines()

    # 获取类别
    for line in lines:
        cat = line.split('\n')[0]
        i += 1
        key.append(str(i - 1))
        value.append(cat)
    category = dict(zip(key, value))  # demo:{'0': 'yes', '1': 'no'}

    if not os.path.exists(result_path):
        os.makedirs(result_path)

    # 分类别存个数
    for root, dir, files in os.walk(label_path):
        for file in tqdm(files):
            label_ = os.path.join(root, file)
            with open(label_, 'r') as f:
                l = f.readlines()
                for k in l:
                    lb_class = k.split(' ')[0]        # 类别序号 0
                    lb_category = category[lb_class]  # 类别名称 yes
                    path = os.path.join(result_path, lb_category + '.txt')  # 生成各个类别的txt
                    with open(path, 'a') as f2:
                        try:  # 防止有的label 为空
                            line_write = file[:-4] + k[1:]  # 将每一行写入txt文件，格式为：文件名 中心点x，中心点y，x/图片宽，y/图片高
                            f2.write(line_write)
                        except TypeError:
                            continue
    f2.close()
    print('转换完成')

    for root, dir, files in os.walk(result_path):
        for name in files:  # dfhifvuer5.txt
            txt_path = os.path.join(root, name)
            txt = open(txt_path)
            num = len(txt.readlines())
            if num != 0:
                label_count[name[:-4]] = num
                # print(name[:-4], num)  # yes 55
            else:
                continue

#函数调用
get_path()
map(model_path['data'],model_path['cfg'],model_path['weights'],path)
log_path = path + '/map.logs'
get_map(log_path)
count_label(test_path,model_path['name'])

report_dict['map'] = map_re
report_dict['label_count'] = label_count

json_path = os.path.join(save_json,'record.json')
with open(json_path,"w") as f:
    json.dump(report_dict, f,indent=4,ensure_ascii=False)
    print("加载入文件完成...")




