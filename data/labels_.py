import copy
import os


def takeFirst(elem):
    return elem[2]


def read_label(path):
    l_x, l_y, l_w, l_h, line_list = [], [], [], [], []
    x_r,y_r = [],[]
    if not os.path.getsize(path):
        # print('内容为空！')
        return []
    else:
        with open(path, 'r')as f:
            for line in f.readlines():
                line = line.strip('\n')  # 去掉列表中每一个元素的换行符
                line_ = line.split(" ")

                xleft = float(line_[1])-float(line_[3])/2
                xright = float(line_[1])+float(line_[3])/2
                yleft = float(line_[2]) - float(line_[4]) / 2
                yright = float(line_[2]) + float(line_[4]) / 2
                l_x.append((line_[1], line_[3],xleft))  # (x,x/w)
                x_r.append((line_[1], line_[3], xright))

                # l_x.append((line_[1], line_[3]))   #(x,x/w)
                l_y.append((line_[2], line_[4],yleft))
                y_r.append((line_[2], line_[4], yright))
                line_list.append(line_)
            l_x_s, l_y_s = copy.deepcopy(l_x), copy.deepcopy(l_y)
            l_x_s.sort(reverse=False, key=takeFirst)  #以x_center的大小做判断,升序-->改为以xleft
            l_y_s.sort(reverse=False, key=takeFirst)
            x_r.sort(reverse=False, key=takeFirst)
            y_r.sort(reverse=False, key=takeFirst)
            x_big, y_big, x_small, y_small = x_r[-1], y_r[-1], l_x_s[0], l_y_s[0]
            return x_small, y_small, x_big, y_big, line_list


# if __name__ == "__main__":
#     Path = r'/home/fei/file_w/code/Data_enhance/label/0aa71591-468d-4ae5-a30d-16834d56e95f.txt'
#     print(read_label(Path))
