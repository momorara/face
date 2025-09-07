"""
2025/08/12
人間の数をカウント
手とかも独立して人間と判定するので、信頼度で足切りできるようにした。
正確な人数は微妙かも、ただ、ちょっと離れた人間はうまくカウントできそう

2025/09/06  USBカメラ対応

"""

from ultralytics import YOLO
import cv2
from picamera2 import Picamera2
from imutils.video import FPS
import time 
import sys

# # カメラ設定
# picam2 = Picamera2()
# config = picam2.create_preview_configuration(main={"size": (640, 480), "format": "RGB888"})
# picam2.configure(config)
# picam2.start()

# USBカメラを初期化
cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, camera_width_x)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_width_y)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# USBカメラが開けたか確認
if not cap.isOpened():
    print("カメラが開けません")
    sys.exit()

cv2.namedWindow("スペースを押して写真を保存", cv2.WINDOW_NORMAL)
cv2.resizeWindow("スペースを押して写真を保存", 640, 480)

print()
print("qキーの入力で終了します。")
time.sleep(1)

# YOLOのモデルを読み込み（nanoモデルを推奨）
model = YOLO("yolo11n.pt")
# model = YOLO("yolov10n.pt")
# model = YOLO("yolov9t.pt")
# model = YOLO("yolov8n.pt")
# model = YOLO("yolov5su.pt")

model_name = model.ckpt_path # モデルファイルのパス
print("yoloモデル:",model_name)  
print()

# FPS計測開始
fps = FPS().start()
while True:
    # カメラから処理するフレームを取得
    # frame = picam2.capture_array()
    ret, frame = cap.read()
    if not ret:
        print("カメラからフレームを取得できませんでした")
        break
    # YOLOで推論（BGR画像そのままでOK）
    results = model(frame)
    # 検出された画像を取得（OpenCV形式のnumpy配列）
    annotated_frame = results[0].plot()
    # 表示
    cv2.imshow(model_name + " Camera", annotated_frame)
    # キー入力待ち（qで終了）
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    # # YOLOで推論（BGR画像そのままでOK）
    # # 進行状況バー（tqdm）表示
    # # results = model(frame)
    # # 進行状況バー（tqdm）非表示
    # results = model(frame, verbose=False)

    # # 人間だけ検出する 検出するクラスを指定する
    # # ただし、modelはそのままなので、スピードは変わらない
    # # results = model(frame, classes=[0], verbose=False)


    # # 検出された画像を取得（OpenCV形式のnumpy配列）
    # annotated_frame = results[0].plot()
    # # 表示 ウィンドウのタイトル
    # cv2.imshow(model_name + " Camera", annotated_frame)

    # # yoloが見つけたクラスの数をターミナルに表示
    # boxes = results[0].boxes

    # class_ids = boxes.cls.cpu().numpy()     # クラスID
    # confidences = boxes.conf.cpu().numpy()  # 信頼度

    # # 条件: クラスID==0(person) かつ 信頼度 >= 0.6
    # mask = (class_ids == 0) & (confidences >= 0.6)
    # person_count = mask.sum()
    # print("人間",person_count)  

    # # キー入力待ち（qで終了）
    # if cv2.waitKey(1) & 0xFF == ord("q"):
    #     break
    fps.update()

# FPS計測終了
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# 終了処理
cv2.destroyAllWindows()
