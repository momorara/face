"""
2025/03/31  テスト

headshotsで撮影された写真に対して
顔を判別して、顔部分を切り出す。
エラーが出た場合は、顔が写っていないと判定されたので、撮り直しをすること

Copyright (c) 2026 takanobu Kawabata
All rights reserved.
"""

import os
import cv2
import dlib

def extract_faces(dataset_dir="dataset", result_dir="result"):    
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    
    detector = dlib.get_frontal_face_detector()
    
    for person_name in os.listdir(dataset_dir):
        person_path = os.path.join(dataset_dir, person_name)
        if "/._" in person_path:  # 隠しファイルをスキップ
            continue
        # print(person_path)
        if os.path.isdir(person_path):
            for file in os.listdir(person_path):
                img_path = os.path.join(person_path, file)
                img = cv2.imread(img_path)
                if "/.DS_Store" in img_path:  # 隠しファイルをスキップ
                    continue
                if "/._" in img_path:  # 隠しファイルをスキップ
                    continue
                if img is None:
                    print("顔が見つかりません",img_path)
                    continue
                
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector(gray)
                # print(faces)
                if len(faces) == 0 :
                    print("顔が見つかりません",img_path)
                    continue
                for i, face in enumerate(faces):
                    x, y, w, h = face.left(), face.top(), face.width(), face.height()
                    face_img = img[y:y+h, x:x+w]
                    save_path = os.path.join(result_dir, f"{person_name}_{i}.jpg")
                    cv2.imwrite(save_path, face_img)
                    print(f"Saved: {save_path}")

if __name__ == "__main__":
    extract_faces()
