import cv2 as cv
import sys
import time, datetime
import numpy as np
import argparse

ip_url = "rtsp://210.99.70.120:1935/live/cctv017.stream"
cap = cv.VideoCapture(ip_url)

parser = argparse.ArgumentParser(description='control the fps')
parser.add_argument('--fps', help='contorl the fps value', default=int(cap.get(cv.CAP_PROP_FPS) / 10000))
parser.add_argument('--time', help='contorl the recording time', default=10)

args = parser.parse_args()
if not cap.isOpened():
    print(cap.isOpened())
    sys.exit()

width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

fps = int(args.fps)
print('fps', fps)

record_t = int(args.time)
print(f"Recording time: {record_t} sec")

fourcc = cv.VideoWriter_fourcc('X', 'V', 'I', 'D')
out = cv.VideoWriter('./recorder.mp4', fourcc, fps, (width, height))

print("Processing...")
start_time = time.time()

mode = 'normal'
while True:
        
    ret, frame = cap.read()
    
    if not ret:
        print('프레임 읽을 수 없음')
        break
    
    if mode == 'record':
        radius = 15
        cv.circle(frame, (width - (radius * 2) , height - (radius * 2)), radius, (255, 0, 255), -1)
        out.write(frame)
        
    cv.imshow('streaming video', frame)

    now = datetime.datetime.now().strftime("%d_%H-%M-%S")
    
    if time.time() - start_time >= record_t:
        break
    
    k = cv.waitKey(1) & 0xff
    if k == 27:
        break
    
    elif k == ord('r'):
        mode = 'record'
        print("Mode changed to record")
        
    elif k == ord('n'):
        mode = 'normal'
        print("Mode changed to normal")
        
    elif k == ord('c'):
        print("캡쳐")
        cv.imwrite("./" + str(now) + ".png", frame)

    elif k == 32:
        if mode == 'normal':
            mode = 'record'
            print("Mode changed to record via Space key")
        else:
            mode = 'normal'
            print("Mode changed to normal via Space key")
            
    
cap.release()
out.release()
cv.destroyAllWindows()
print("END!")