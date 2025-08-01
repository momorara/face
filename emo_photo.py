
"""
pip install deepface
pip install tf-keras
"""
from deepface import DeepFace

# 指定したパスの写真に対して感情分析します。
result = DeepFace.analyze(img_path = "akio/image_0.jpg", actions = ['emotion'])
#print(result[0]['emotion'])  # {'happy': 95.4, 'neutral': 3.2, ...}


"""
アウトプットは
{'angry': 5.434974923446134e-05, 'disgust': 2.8185748845999115e-06, 'fear': 0.0021737752831541,
 'happy': 97.52634763717651, 'sad': 0.02232246770290658, 'surprise': 2.350001153672565e-05,
 'neutral': 2.449074387550354}
がはいっている。

日本語にするとともに、数値を整数にする
"""

# 例: result[0]['emotion'] に感情スコア辞書が入っている
emotion_scores = result[0]['emotion']

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