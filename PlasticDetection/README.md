python test.py --data data.yaml --img 416 --conf 0.40  --weights ./yolov5-weights/weights/best.pt

python detect.py --source deeptrash/mytest/images/1.jpg --weights ./yolov5-weights/weights/best.pt --img 416
python detect.py --source sample_video.mp4 --weights ./yolov5-weights/weights/best.pt --img 416
python detect.py --source sample_video_2.mp4 --weights ./yolov5-weights/weights/best.pt --img 416
python detect.py --source 0 --weights ./yolov5-weights/weights/best.pt --img 416
