from PIL import Image
import cv2
image=Image.open('/home/fei/Desktop/test/test/images/1.jpg')
# image = Image.open(img_path)
image = image.convert('RGB')
w, h = image.size
print(w,h)
background = Image.new('RGB', size=(max(w, h), max(w, h)), color=(0, 0,0))  # 创建背景图，颜色值为127
length = int(abs(w - h) // 2)  # 一侧需要填充的长度
box = (length, 0) if w < h else (0, length)  # 粘贴的位置
background.paste(image, box)          #背景图.past(前景图，位置（左上角，右下角）)
# background.show()
# image_data=image.resize((768,768))#缩放
image_data =background.resize((768, 768))
# image_data.show()
# image_data.save(save_path + '/' + name)
background.save('/home/fei/Desktop/test/test/images/2.jpg')
# image_data.save('/home/fei/Desktop/test/888.jpg')

# img1 = cv2.imread('/home/fei/Desktop/test/8.jpg')
# img2 = cv2.imread('/home/fei/Desktop/test/88.jpg')
# img3 = cv2.imread('/home/fei/Desktop/test/888.jpg')
# cv2.namedWindow('2', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('2', 800, 2000)  # 改变窗口大小
# cv2.imshow('2', img2)
# cv2.waitKey(0)

