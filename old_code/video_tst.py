import cv2 as cv

#cap = cv.VideoCapture('/data/video/D13_20200506145527.mp4')
#cap = cv.VideoCapture('/data/video/D08_20200504005857.mp4')
cap = cv.VideoCapture('/data/ppg/raw/20200806/D04_20200802235959.mp4')
#cap = cv.VideoCapture('rtsp://wd:wd@172.22.4.198:554/cam/realmonitor?channel=1&subtype=0')

while True:
    _, f = cap.read()
    cv.imshow('Cap', cv.resize(f, (0, 0), fx=0.5, fy=0.5))
    cv.waitKey(1)
