from ultralytics import YOLO
import cv2
from   picamera2 import Picamera2
from imutils.video import FPS
import time 

# カメラ設定
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (640, 480), "format": "RGB888"})
picam2.configure(config)
picam2.start()


print()
print("qキーの入力で終了します。")
time.sleep(1)

# YOLOのモデルを読み込み（nanoモデルを推奨）
model = YOLO("yolo11n.pt")
# model = YOLO("yolov10n.pt")
# model = YOLO("yolov9t.pt")
# model = YOLO("yolov8n.pt")
model_name = model.ckpt_path # モデルファイルのパス
print("yoloモデル:",model_name)  
print()

# FPS計測開始
fps = FPS().start()
while True:
    # カメラから処理するフレームを取得
    frame = picam2.capture_array()
    # YOLOで推論（BGR画像そのままでOK）
    results = model(frame)
    # 検出された画像を取得（OpenCV形式のnumpy配列）
    annotated_frame = results[0].plot()
    # 表示
    cv2.imshow(model_name + " Camera", annotated_frame)
    # キー入力待ち（qで終了）
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    fps.update()
# FPS計測終了
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# 終了処理
cv2.destroyAllWindows()
