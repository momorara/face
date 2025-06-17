"""
モデルに含まれるカテゴリーを表示します。
"""
from ultralytics import YOLO
model = YOLO("yolov8n.pt")
print(model.names)