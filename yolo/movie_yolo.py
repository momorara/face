"""
2025/08/12
人間の数をカウント
手とかも独立して人間と判定するので、信頼度で足切りできるようにした。
正確な人数は微妙かも、ただ、ちょっと離れた人間はうまくカウントできそう

対応動画フォーマットの例（OpenCV依存）
MP4 (.mp4)
AVI (.avi)
MOV (.mov)
MKV (.mkv)
WebM (.webm)
FLV (.flv)
WMV (.wmv)
"""
from ultralytics import YOLO
import cv2
from picamera2 import Picamera2
from imutils.video import FPS
import time 

print()
print("qキーの入力で終了します。")
time.sleep(1)

# YOLOのモデルを読み込み（nanoモデルを推奨） 2025/8時点対応モデル
model = YOLO("yolo11n.pt")
# model = YOLO("yolov10n.pt")
# model = YOLO("yolov9t.pt")
# model = YOLO("yolov8n.pt")

model_name = model.ckpt_path # モデルファイルのパス
print("yoloモデル:",model_name)  

# 動画ファイルを開く
video_path = "parson_640x360.mp4"
#video_path = "Animals3.m4v"
#video_path = "5_ume.mp4"
#video_path = "5_maturi.mp4"

cap = cv2.VideoCapture(video_path)
print("movie_file:",video_path)  
print()

# FPS計測開始
fps = FPS().start()
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break  # 動画終了

    # YOLOで推論（BGR画像そのままでOK）
    # 進行状況バー（tqdm）表示
    results = model(frame)

    # 進行状況バー（tqdm）非表示
    # 人間だけ検出する 検出するクラスを指定する
    # ただし、modelはそのままなので、スピードは変わらない
    # results = model(frame, classes=[0], verbose=False)

    # 検出された画像を取得（OpenCV形式のnumpy配列）
    annotated_frame = results[0].plot()
    # 表示 ウィンドウのタイトル
    cv2.imshow(model_name + " Movie", annotated_frame)

    # yoloが見つけたクラスの数をターミナルに表示
    boxes = results[0].boxes
    class_ids = boxes.cls.cpu().numpy()     # クラスID
    confidences = boxes.conf.cpu().numpy()  # 信頼度

    # 条件: クラスID==0(person) かつ 信頼度 >= 0.6
    # mask = (class_ids == 0) & (confidences >= 0.6)
    mask = (confidences >= 0.6)
    person_count = mask.sum()
    #print("人間",person_count)  


    # キー入力待ち（qで終了）
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    fps.update()

# FPS計測終了
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# 終了処理
cap.release()
cv2.destroyAllWindows()
