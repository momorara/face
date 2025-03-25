# -*- coding: utf-8 -*-
#!/usr/bin/python3
"""
2025/03/11  画像の大きさなどを本体プログラムを変更せずに
            設定できるようにする
"""
# カメラから取り込む画像の大きさの設定
# headshots,facial_reqで使用
def camera_width():
    camera_width_x = 640
    camera_width_y = 480
    # camera_width_x = int(640*1.5)
    # camera_width_y = int(480*1.5)
    return camera_width_x , camera_width_y

# 処理用の画像の大きさの設定
# headshotsで使用
def proces_width():
    proces_width_x = 640
    proces_width_y = 480
    # proces_width_x = int(640*0.5)
    # proces_width_y = int(480*0.5)
    return proces_width_x , proces_width_y

# 画面に出す画像の大きさ
# 不使用
def disp_width():
    disp_width_x = 640
    disp_width_y = 480
    return disp_width_x , disp_width_y

# 検出する顔の最小大きさ デフォルト 50
def face_size():
    return 200
    # camera_widthに対しての大きさ
    # 小さいと離れた人の顔も認識してしまうので、近くの人だけ認識させる

# 必要な連続検出回数 デフォルト 5
def necessary_count():
    return 2
    # taguchモデルでは不使用

def speed_size():
    return 0.6
    # 1で640*480のまま処理
    # 0.5で320*240で処理高速化になる

"""
tolerance を下げる（例：0.4）と誤認識が減るが、認識されにくくなる
tolerance を上げる（例：0.7）と認識されやすいが、誤認識が増える
デフォルト0.6
"""
def tolerance_parameter():
    return 0.6

# 田口モデルを使用する場合は 1
def model_choice():
    return 1

"""
# 顔を近づけて写すなら上記ほど大きくなくて良いような気がする。
# それにスピードが速くなると思う
# ただし、精度はどうかな?
"""
# # カメラから取り込む画像の大きさの設定
# def camera_width():
#     camera_width_x = 300
#     camera_width_y = 300
#     return camera_width_x , camera_width_y

# # 処理用の画像の大きさの設定
# def proces_width():
#     proces_width_x = 300
#     proces_width_y = 300
#     return proces_width_x , proces_width_y

# # 画面に出すがぞうの大きさ
# def disp_width():
#     disp_width_x = 300
#     disp_width_y = 300
#     return disp_width_x , disp_width_y
