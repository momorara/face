#! /usr/bin/python
# headshots.py

"""
2025/03/08  Bullseyeへ変換
            終了はecs
2025/03/11  画像サイズをconfigで設定
2025/03/30  組み合わせテスト 
2025/07/25  カメラタイプ対応 *1

headshots_OnePerson_01.py
    パイカメラv1.3を使い一人分の顔写真を撮影する。
    プログラムを起動すると名前を聞いてくるので、入力すると撮影モードになる(名前は半角英数字のみ)
    スペースキーでシャッターを切る
    ESCかqキーが押されたらプログラム終了

headshots_OnePerson.pyを改造して感情分析プログラムにする
2025/07/31  deepfaceの使用
            deepfaceのライセンスはMITです。
            https://github.com/serengil/deepface
            age,genderを入れると遅いし、フリーズする
2025/08/01  インストール方法を確認
"""
import os
import sys
import cv2
from   picamera2 import Picamera2
import config
# *1
from libcamera import controls

"""　感情分析
pip install deepface
pip install tf-keras
"""
from deepface import DeepFace

# カメラタイプの取り込み *1
camera_type  = config.camera_type()
# カメラから取り込む画像の大きさの設定
camera_width_x , camera_width_y  = config.camera_width()
# 処理用の画像の大きさの設定
proces_width_x , proces_width_y  = config.proces_width()

# Picamera2 を使用
picam2 = Picamera2()
# config = picam2.create_preview_configuration(main={"size": (640, 480)})
# 色がおかしかったので、修正
config = picam2.create_preview_configuration(main={"size": (camera_width_x, camera_width_y), "format": "RGB888"})
picam2.configure(config)
if camera_type == 3:
    # オートフォーカスを有効にする *1
    picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
picam2.start()

cv2.namedWindow("スペースを押して写真を保存", cv2.WINDOW_NORMAL)
# cv2.resizeWindow("press space to take a photo", 500, 300)
cv2.resizeWindow("スペースを押して写真を保存", proces_width_x, proces_width_y)

img_counter = 0

while True:
    frame = picam2.capture_array()
    # frame = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR)
    cv2.imshow("スペースを押して写真を保存", frame)

    k = cv2.waitKey(1)
    if k%256 == 27 or k%256 == 113: #ESCかqキーが押されたら終了
        # ESCキーが押されたら終了
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # スペースキーが押されたら写真を保存
        img_name = "emo_photo.jpg"
        cv2.imwrite(img_name, frame)
        print(f"{img_name} written!")

        # ここから感情分析
        # 指定したパスの写真に対して感情分析します。
        try:
            # result = DeepFace.analyze(img_name, actions = ['emotion','age', 'gender'])
            result = DeepFace.analyze(img_name, actions = ['emotion'])
        
            #print(result[0]['emotion'])  # {'happy': 95.4, 'neutral': 3.2, ...}
            # 例: result[0]['emotion'] に感情スコア辞書が入っている
            emotion_scores = result[0]['emotion']
            # age_scores = result[0]['age']
            # gender_scores = result[0]['gender']
            # 英語→日本語変換マップ
            emotion_map = {
                'angry': '怒り',
                'disgust': '嫌悪',
                'fear': '恐怖',
                'happy': '喜び',
                'sad': '悲哀',
                'surprise': '驚き',
                'neutral': '中立'
            }
            # 数値を四捨五入で整数化して日本語ラベルに変換
            result_jp = {emotion_map.get(k, k): round(v) for k, v in emotion_scores.items()}

            # 表示
            for emotion, score in result_jp.items():
                print(f"{emotion}: {score}%")

            # 最大の感情を取得
            max_emotion_eng = max(emotion_scores, key=emotion_scores.get)
            max_emotion = emotion_map.get(max_emotion_eng, max_emotion_eng)
            max_score = round(emotion_scores[max_emotion_eng])
            print()
            print(f"最も強い感情: {max_emotion} ({max_score}%)")

            # print(age_scores,gender_scores)

        except:
            print("顔を認識できませんでした。もう一度")

        print("スペースキーで実行")

cv2.destroyAllWindows()
