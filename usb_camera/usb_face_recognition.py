#! /usr/bin/python
# headshots.py

"""
2025/07/25  usbカメラ仕様に変更した
"""

import config
# tolerance_parameterの取得 精度調整用
tolerance_para = config.tolerance_parameter()
print("tolerance_parameter =", tolerance_para)
print("ウォームアップ中ちょっと待って\n")

import dlib
import cv2
import time
from imutils.video import FPS
import pickle
import multiprocessing
from scipy.spatial.distance import euclidean  # ユークリッド距離

# 設定の取得
camera_type  = config.camera_type()
camera_width_x, camera_width_y = config.camera_width()
disp_width_x, disp_width_y = config.disp_width()  # 現在未使用
face_size_para = config.face_size()
necessary_count = config.necessary_count()        # 現在未使用
speed_size = config.speed_size()
model_choice = config.model_choice()

# Dlib モデル読み込み
face_detector = dlib.get_frontal_face_detector()
if model_choice == 1:
    face_rec_model_path = "./face_dat/taguchi_face_recognition_resnet_model_v1.dat"
else:
    face_rec_model_path = "./face_dat/dlib_face_recognition_resnet_model_v1.dat"
face_rec_model = dlib.face_recognition_model_v1(face_rec_model_path)
shape_predictor = dlib.shape_predictor("./face_dat/shape_predictor_68_face_landmarks.dat")

# エンコーディング読み込み
currentname = "unknown"
encodingsP = "./face_dat/encodings_taguchi.pickle"
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(encodingsP, "rb").read())

def process_faces(rgb_frame, gray_frame, tolerance, face_size):
    faces = face_detector(gray_frame, 1)
    encodings = []
    names = []

    for face in faces:
        width = face.right() - face.left()
        height = face.bottom() - face.top()
        if width < face_size or height < face_size:
            continue

        shape = shape_predictor(gray_frame, face)
        encoding = face_rec_model.compute_face_descriptor(rgb_frame, shape)
        encodings.append(encoding)

        distances = [euclidean(encoding, known) for known in data["encodings"]]
        min_distance = min(distances)
        if min_distance < tolerance:
            name = data["names"][distances.index(min_distance)]
        else:
            name = "Unknown"
        names.append(name)

    return faces, names

if __name__ == "__main__":
    # USBカメラ起動
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, camera_width_x)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_width_y)

    if not cap.isOpened():
        print("カメラが開けません。")
        exit()

    time.sleep(2.0)  # ウォームアップ

    fps = FPS().start()
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

    proces_width_x = int(camera_width_x * speed_size)
    proces_width_y = int(camera_width_y * speed_size)
    face_size_para = face_size_para * speed_size

    while True:
        ret, frame = cap.read()
        if not ret:
            print("カメラフレームを取得できませんでした。")
            break

        small_frame = cv2.resize(frame, (proces_width_x, proces_width_y))
        gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
        rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        result_async = pool.apply_async(process_faces, (rgb, gray, tolerance_para, face_size_para))
        faces, names = result_async.get()

        for (face, name) in zip(faces, names):
            (top, right, bottom, left) = (face.top(), face.right(), face.bottom(), face.left())
            top, right, bottom, left = [int(val * (camera_width_x / proces_width_x)) for val in [top, right, bottom, left]]
            y = top - 15 if top - 15 > 15 else top + 15

            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            thickness = 4 if name != "Unknown" else 6
            cv2.rectangle(frame, (left, top), (right, bottom), color, thickness)
            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

            if name != currentname:
                currentname = name
                print(currentname)

            if name == currentname and name != "Unknown":
                print("ok")

        cv2.imshow("Facial Recognition is Running", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q") or key == 27:
            break
        if key == ord("p"):
            cv2.imwrite("face_" + currentname + ".jpg", frame)

        fps.update()

    fps.stop()
    print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    cap.release()
    cv2.destroyAllWindows()
    pool.close()
    pool.join()
