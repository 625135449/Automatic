# Automatic

### Requirements

```shell
pip3 install -r requirements.txt
```

## Two main file

### main_auto.py：

1.该文件可以全自动实现所有功能

2.要求文件格式：xxx(dir)----xxx(dir,存放图片)、xxx(dir,存放darknet格式的txt文件)、xxx(file，存放下载好的平台格式的json)


### main_function.py：

1.该文件可以实现手动选择需要的各个功能：

+ 检查各个文件夹下的文件数量

+ 制作labels：即将平台下载好的json转换为darknet格式的txt文件，带helmet表示安全帽的标签转换格式，标签扩大了10%

+ 标签映射：平台上的标签索引改为各个模型需要的索引

+ 数据增强：对平台上的白框进行随机裁剪操作：可增强至原始数据的1~2倍

+ 制作测试集：对数据集按2：8分，2：测试集，8：训练集

## How to use

### main_auto.py(使用该功能前需配置相应的nfs环境）：

1.选择需要的文件夹

2.选择需要的模型（会自动实现以下功能):
 + 将本地选择的文件夹复制到相应人员的share文件夹下（share下的模型文件夹，ex:Helmet）
 + share下的Helmet文件夹晖自动创建当天的文件夹，ex：Helmet_20210805，该文件夹的结构如下：
 images(dir)、labels(dir)、save(dir)、xxx.json
 + 对于save(dir），save中放的为训练数据，其结构为：images(dir)、labels(dir)、log(dir)、test(dir)、val(dir)，
训练前先对val中的十张图片进行人工审查
 
3.当出现拷贝完成并且不报错，为运行成功

### main_function.py：
1.选择需要的文件夹

2.选择需要的功能序号即可

3.功能完成后选择序号0即可退出程序
