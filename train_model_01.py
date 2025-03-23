#! /usr/bin/python
"""
2025/03/08  Bullseyeへ変換
2025/03/14  高速化を試したが
            multiprocessing 遅くなった
            GPU さらに遅くなった
            サイズを小さく 速くなるが精度はどうかな
            0.5にしてみたがfaceではスピードは変わらなかった
2025/03/17  田口モデルように改造 処理が速くなった
2025/03/18  データ置き場を整理
"""

print("ウォームアップ中、しばらくお待ちください...")
# 必要なライブラリをインポート
import dlib
import pickle
import cv2
import os
from imutils import paths
import time
start_Time = time.time()

# 事前学習済みのTaguchiモデルを読み込む
print("[INFO] Taguchiモデルを読み込んでいます...")
taguchi_model = dlib.face_recognition_model_v1("./face_dat/taguchi_face_recognition_resnet_model_v1.dat")
shape_predictor = dlib.shape_predictor("./face_dat/shape_predictor_68_face_landmarks.dat")

# Dlibの顔検出器
detector = dlib.get_frontal_face_detector()

# 画像が保存されているフォルダを指定
print("[INFO] 顔データの処理を開始します...")
imagePaths = list(paths.list_images("dataset"))

# 顔のエンコーディングと名前を保存するリストを初期化
knownEncodings = []
knownNames = []

# 画像パスを順番に処理
for (i, imagePath) in enumerate(imagePaths):
    if "/._" in imagePath:  # 隠しファイルをスキップ
        continue

    # 画像のファイルパスから人物名を取得
    print("[INFO] {}/{} の画像を処理中: {}".format(i + 1, len(imagePaths), imagePath))
    name = imagePath.split(os.path.sep)[-2]

    # 画像を読み込み、OpenCVのBGR形式からdlib用のRGB形式に変換
    image = cv2.imread(imagePath)
    if image is None:
        print(f"[WARNING] 画像を読み込めませんでした: {imagePath}")
        continue

    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 画像内の顔を検出
    faces = detector(rgb_image)
    if len(faces) == 0:
        print(f"[WARNING] 顔が検出されませんでした: {imagePath}")
        continue

    # 最初に見つかった顔の特徴量を取得
    face = faces[0]
    landmarks = shape_predictor(rgb_image, face)
    encoding = taguchi_model.compute_face_descriptor(rgb_image, landmarks)

    # エンコーディング結果を保存
    knownEncodings.append(encoding)
    knownNames.append(name)

# 顔のエンコーディングデータをファイルに保存
print("[INFO] エンコーディングデータを保存します...")
data = {"encodings": knownEncodings, "names": knownNames}
with open("./face_dat/encodings_taguchi.pickle", "wb") as f:
    f.write(pickle.dumps(data))

print("処理が完了しました。")
run_Time = time.time() - start_Time
print(run_Time)