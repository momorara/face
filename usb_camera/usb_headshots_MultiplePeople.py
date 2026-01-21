#! /usr/bin/python
# headshots.py

"""
2025/07/25  usbカメラ仕様に変更した
Copyright (c) 2026 takanobu Kawabata
All rights reserved.
"""
import os
import cv2
import config

# カメラタイプの取り込み（未使用でも残してOK）
camera_type = config.camera_type()

def capture_photos(name):
    try:
        userDirPath = f"dataset/{name}"
        os.mkdir(userDirPath)
    except FileExistsError:
        print("Datasets already exist.")

    # カメラと解像度の設定
    camera_width_x, camera_width_y = config.camera_width()
    proces_width_x, proces_width_y = config.proces_width()

    # USBカメラを初期化
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, camera_width_x)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, camera_width_y)

    if not cap.isOpened():
        print("USBカメラが開けませんでした。")
        return

    cv2.namedWindow("スペースを押して写真を保存", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("スペースを押して写真を保存", proces_width_x, proces_width_y)

    img_counter = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print("カメラ画像を取得できませんでした。")
            break

        cv2.imshow("スペースを押して写真を保存", frame)

        k = cv2.waitKey(1)
        if k % 256 == 27:  # ESCキー
            print("撮影終了。次の人の登録へ...")
            break
        elif k % 256 == 32:  # スペースキー
            img_name = f"dataset/{name}/image_{img_counter}.jpg"
            cv2.imwrite(img_name, frame)
            print(f"{img_name} written!")
            img_counter += 1

    cap.release()
    cv2.destroyAllWindows()

# ユーザー入力ループ
while True:
    name = input("あなたの名前をローマ字で登録してください (終了するには 'end' と入力): ")
    if name.lower() in ["end", "exit", "quit"]:
        print("プログラムを終了します。")
        break
    capture_photos(name)
    print("")
