from PR.cal import main1
import time
if __name__=='__main__':
    #代码中改变的：iou阈值；最多30个类，在画图那块颜色显示；类别阈值20个
#darknet的输出
    output_labels = r'/media/vs/Data/darknet_train_result/darknet/Helmet/helmet_new/Tiny/data/all_test/GT/'
    # output_labels = r'/media/vs/Data/darknet_train_result/darknet/Helmet/helmet_top/PR/all_test/GT/'
    mask_name = r'/media/vs/Data/darknet_train_result/darknet/Helmet/helmet_new/Tiny/model/20210721/name.txt'
    DT = r'/home/fei/darknet/results/'
    start1=time.time()
    main1(output_labels,mask_name,DT)
    final1=time.time()
    print('time',str(final1-start1))
#tensorrt的输出
    # output_labels1 = r'/media/vs/Data/darknet_train_result/darknet/Helmet/helmet_new/Tiny/data/all_test/GT/'
    # mask_name1 = r'/media/vs/Data/darknet_train_result/darknet/Helmet/helmet_new/Tiny/model/20210721/name.txt'
    # tensorrt_output = r'/home/fei/darknet/results/comp4_det_test_no helmet.txt'
    # start2=time.time()
    # main2(output_labels1,mask_name1,tensorrt_output)
    # final2=time.time()
    # print('time',str(final2-start2))
    # print('test')