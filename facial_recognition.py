#! /usr/bin/python
"""
2025/03/08  Bullseyeへ変換
            終了はesc
2025/03/11  画像サイズをconfigで設定
2025/03/12  toleranceパラメータを設定
2025/03/14  ・multiprocessingによる高速化 倍近いスピードアップした
            マルチプロセスを使う関係上 if __name__ == "__main__":に
            プログラムを書く必要があり、改造がしにくい感がある
            ・検出する顔の大きさを設定できるようにする
            これにより小さい顔は検出しない ひとりで大きく映る場合はちょうど良い
2025/03/25  日本人の精度を上げるため田口モデルを適用
            データ置き場を整理
            処理軽減のパラメータをconfig化
2025/03/30  モデルを選択できるようにした
2025/03/31  コメント整理   
2025/04/17  プログラム名を顔識別　face_recognitionとした
2025/07/25  カメラタイプ対応 *1

face_recognition.py
    01

Copyright (c) 2026 takanobu Kawabata
All rights reserved.
"""
import config
# tolerance_parameterの取得 精度調整用
tolerance_para = config.tolerance_parameter()
print("tolerance_parameter=",tolerance_para)
print("ウォームアップ中ちょっと待って")
print()

import dlib
import cv2
import time
from imutils.video import FPS
import pickle
import multiprocessing
from picamera2 import Picamera2
from scipy.spatial.distance import euclidean  # Euclidean distanceを使用
# *1
from libcamera import controls

# 設定の取得
# カメラタイプの取り込み *1
camera_type  = config.camera_type()
# カメラから取り込む画像の大きさの設定
camera_width_x, camera_width_y = config.camera_width()
# 処理用の画像の大きさの設定
disp_width_x, disp_width_y = config.disp_width()  # 現在使っていない
# 検出する顔の最小大きさ
face_size_para = config.face_size() 
# 必要な連続検出回数
necessary_count = config.necessary_count()    # 現在使っていない
# 処理性能軽減のための画像サイズ縮小
speed_size = config.speed_size()  

# Dlibの顔検出器
face_detector = dlib.get_frontal_face_detector()

# 
model_choice = config.model_choice() 
# 汎用モデル
face_rec_model_path = "./face_dat/dlib_face_recognition_resnet_model_v1.dat"
# 田口モデル
if model_choice == 1:
    face_rec_model_path = "./face_dat/taguchi_face_recognition_resnet_model_v1.dat"
face_rec_model = dlib.face_recognition_model_v1(face_rec_model_path)
# 顔検出器 特徴量を取得
shape_predictor = dlib.shape_predictor("./face_dat/shape_predictor_68_face_landmarks.dat")


# 初期化
currentname = "unknown"
encodingsP = "./face_dat/encodings_taguchi.pickle"
print("[INFO] loading encodings + face detector...")

# pickleの読み込み
data = pickle.loads(open(encodingsP, "rb").read())

def process_faces(rgb_frame, gray_frame, tolerance, face_size):
    """顔検出と顔認識を並列処理"""
    # 顔検出
    faces = face_detector(gray_frame, 1)
    encodings = []
    names = []

    for face in faces:
        # 顔の領域の幅と高さを取得
        width = face.right() - face.left()
        height = face.bottom() - face.top()

        # 最小顔サイズより小さい顔を無視
        if width < face_size or height < face_size:
            continue

        # 顔を検出
        shape = shape_predictor(gray_frame, face)
        encoding = face_rec_model.compute_face_descriptor(rgb_frame, shape)
        encodings.append(encoding)

        # 顔識別
        distances = []
        for known_encoding in data["encodings"]:
            # Euclidean距離を計算
            distance = euclidean(encoding, known_encoding)
            distances.append(distance)

        # 最も近い顔を選択
        min_distance = min(distances)
        if min_distance < tolerance:
            name = data["names"][distances.index(min_distance)]
        else:
            name = "Unknown"
        
        names.append(name)

    return faces, names

if __name__ == "__main__":
    # カメラ設定
    picam2 = Picamera2()
    cam_config = picam2.create_preview_configuration(main={"size": (camera_width_x, camera_width_y), "format": "RGB888"})
    picam2.configure(cam_config)

    if camera_type == 3:
        # オートフォーカスを有効にする *1
        picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
        
    picam2.start()

    time.sleep(2.0)  # Camera warm-up

    # FPS計測開始
    fps = FPS().start()

    # 並列処理用プールを作成
    num_processes = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_processes)

    # 処理負荷を下げるため縮小
    # デフォルトでは、640*480の画像だが、処理時にリサイズして処理
    # 小さい値にするとスピードアップになるが、やりすぎると精度が落ちる
    proces_width_x = int(640 * speed_size)
    proces_width_y = int(480 * speed_size)
    # face_sizeとの関係があるので調整
    face_size_para = face_size_para * speed_size

    while True:
        frame = picam2.capture_array()
        
        # small_frame = cv2.resize(frame, (320, 240))  # 処理負荷を下げるため縮小
        small_frame = cv2.resize(frame, (proces_width_x, proces_width_y))  # 処理負荷を下げるため縮小
        gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
        rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # 並列処理で顔を検出・認識
        result_async = pool.apply_async(process_faces, (rgb, gray, tolerance_para, face_size_para))
        faces, names = result_async.get()

        for (face, name) in zip(faces, names):
            (top, right, bottom, left) = (face.top(), face.right(), face.bottom(), face.left())
            # 座標を元のサイズにスケールアップ
            # top, right, bottom, left = [int(val * (camera_width_x / 320)) for val in [top, right, bottom, left]]
            top, right, bottom, left = [int(val * (camera_width_x / proces_width_x)) for val in [top, right, bottom, left]]
            y = top - 15 if top - 15 > 15 else top + 15

            if name != "Unknown":# 名前が判別できた時は 緑の枠
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 4)
                cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            else: # Unknown の場合は 赤の枠
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 225), 6)
                cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

            if name != currentname:
                currentname = name
                print(currentname)


            """ """ """ """ """ """ """ """ """ """ """ """ 
            """ ここで、名前を確定した場合の処理を入れることが可能 """

            if name == currentname and name != "Unknown":# 2回 連続して同じ名前ならokとプリントする
                print("ok")

            """ """ """ """ """ """ """ """ """ """ """ """ 
            """ """ """ """ """ """ """ """ """ """ """ """ 


        cv2.imshow("Facial Recognition is Running", frame)

        # q or ESCキーが押されたら終了
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q") or key == 27:
            break

        # 'p' キーが押されたら画像保存
        if key == ord("p"):
            cv2.imwrite("face_" + name +".jpg", frame)

        fps.update()

    # FPS計測終了
    fps.stop()
    print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    cv2.destroyAllWindows()
    pool.close()
    pool.join()
