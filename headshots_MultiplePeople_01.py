#! /usr/bin/python
# headshots.py

"""
2025/03/08  Bullseyeへ変換
            終了はecs
2025/03/11  画像サイズをconfigで設定
2025/03/17  複数人撮影に対応
            撮影するにはスペースキーを押す
            一旦終わるにはescキー
            プログラム終了は end exit quit

"""

import os
import cv2
from picamera2 import Picamera2
import config

def capture_photos(name):
    try:
        userDirPath = f"dataset/{name}"
        os.mkdir(userDirPath)
    except FileExistsError:
        print("Datasets already exist.")

    picam2 = Picamera2()
    camera_width_x, camera_width_y = config.camera_width()
    proces_width_x, proces_width_y = config.proces_width()
    
    config_settings = picam2.create_preview_configuration(main={"size": (camera_width_x, camera_width_y), "format": "RGB888"})
    picam2.configure(config_settings)
    picam2.start()
    
    cv2.namedWindow("スペースを押して写真を保存", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("スペースを押して写真を保存", proces_width_x, proces_width_y)
    
    img_counter = 0
    while True:
        frame = picam2.capture_array()
        cv2.imshow("スペースを押して写真を保存", frame)
        
        k = cv2.waitKey(1)
        if k % 256 == 27:  # ESCキーで次の人へ
            print("撮影終了。次の人の登録へ...")
            break
        elif k % 256 == 32:  # スペースキーで写真を保存
            img_name = f"dataset/{name}/image_{img_counter}.jpg"
            cv2.imwrite(img_name, frame)
            print(f"{img_name} written!")
            img_counter += 1
    
    cv2.destroyAllWindows()
    picam2.close()

while True:
    name = input("あなたの名前をローマ字で登録してください (終了するには 'end' と入力): ")
    if name.lower() == "end" or name.lower() == "exit" or name.lower() == "quit":
        print("プログラムを終了します。")
        break
    capture_photos(name)
    print("")
    
