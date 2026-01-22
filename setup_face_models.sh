#!/bin/bash
set -e

BASE_DIR="/home/pi/face/face_dat"
DL_DIR="/tmp/face_models"

#mkdir -p "$BASE_DIR"
mkdir -p "$DL_DIR"

cd "$DL_DIR"
echo
echo "=== dlib 顔認識モデルをセットアップします ==="

download_and_extract () {
    local url="$1"
    local file="$2"

    if [ -f "$BASE_DIR/$file" ]; then
        echo "[SKIP] $file は既に存在します"
        return
    fi

    echo "[DL] $file"
    wget -q "$url" -O "$file.bz2"

    echo "[UNZIP] $file"
    bzip2 -d "$file.bz2"

    mv "$file" "$BASE_DIR/"
}

# 非圧縮モデル用
download_raw () {
    local url="$1"
    local file="$2"

    if [ -f "$BASE_DIR/$file" ]; then
        echo "[SKIP] $file already exists"
        return
    fi

    echo "[DL] $file (raw)"
    wget -q "$url" -O "$BASE_DIR/$file"
}

# # 1. dlib 標準 顔認識モデル
# download_and_extract \
#   "http://dlib.net/files/dlib_face_recognition_resnet_model_v1.dat.bz2" \
#   "dlib_face_recognition_resnet_model_v1.dat"

# 2. 顔ランドマーク
download_and_extract \
  "http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2" \
  "shape_predictor_68_face_landmarks.dat"

# # 3. Taguchi 日本人向け顔認識モデル（GitHub想定）
# download_raw \
#   "https://github.com/TaguchiModels/dlibModels/blob/main/taguchi_face_recognition_resnet_model_v1.7z" \
#   "taguchi_face_recognition_resnet_model_v1.dat"

echo
echo "=== 完了 ==="
echo "配置先: $BASE_DIR"
ls -lh "$BASE_DIR"
echo
