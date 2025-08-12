"""
2025/04/10  写真に対してyoloを実施

プログラムがストーとすると
同じディレクトリ内の.jpgファィルを探し、リストし、プリントする。
次にメッセーを「スペースで次の写真を処理、escで終了します。リターンで実施」として入力待ちになる。
リターンが押されたらリストの最初の写真をyoloし、入力待ちになる。
その後
スペースで次の写真を処理、escで終了
とする

photo_yolo.py
"""
import glob
import cv2
from ultralytics import YOLO

# YOLOv8 モデルを読み込み（適宜 yolov8n.pt や yolov8x.pt に変更可）
# model = YOLO('yolov8n.pt')      # もっとも軽量なモデル 速いが精度劣る
# model = YOLO('yolov8m.pt')    # ミドルなモデル 少し遅くなるが精度上がる
# model = YOLO('yolov8x.pt')    # もっとも大規模なモデル 遅いが精度は良い

# YOLOv11 モデルを読み込み（適宜 yolo11n.pt や yolo11x.pt に変更可）
# model = YOLO('yolo11n.pt')      # もっとも軽量なモデル 速いが精度劣る
# model = YOLO('yolo11.pt')    # ミドルなモデル 少し遅くなるが精度上がる
# model = YOLO('yolo11x.pt')    # もっとも大規模なモデル 遅いが精度は良い

# YOLOのモデルを読み込み（nanoモデルを推奨）
model = YOLO("yolo11n.pt")
# model = YOLO("yolov10n.pt")
# model = YOLO("yolov9t.pt")
# model = YOLO("yolov8n.pt")

# 現在のディレクトリにある .jpg ファイルを取得
image_files = sorted(glob.glob("*.jpg"))

# リスト表示
print("検出されたJPEGファイル:")
for i, file in enumerate(image_files):
    print(f"{i+1}. {file}")

# 最初のメッセージ
input("スペースで次の写真を処理、Escで終了します。リターンで実施 > ")

# 処理ループ
index = 0
while index < len(image_files):
    image_path = image_files[index]
    print(f"\n→ 処理中: {image_path}")

    # YOLOで画像処理
    results = model(image_path)
    for r in results:
        img = r.plot()  # 結果描画済みの画像（NumPy配列）を取得
        cv2.imshow("YOLO Result", img)  # OpenCVで表示

    print("スペースで次の写真を処理、Escで終了")

    # キー入力待ち（cv2.waitKeyで処理）
    while True:
        key = cv2.waitKey(0)
        if key == 27:  # Esc
            print("終了します。")
            exit()
        elif key == 32:  # Space
            index += 1
            break
        else:
            print("スペースキーかEscを押してください。")
cv2.destroyAllWindows()    
print("すべての画像を処理しました。")
