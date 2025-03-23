import os
import glob
from PIL import Image

def combine_images(input_folder, output_folder, output_filename, grid_size=(7, 7), img_size=(140, 140)):
    # 入力フォルダの画像ファイルを取得
    image_paths = sorted(glob.glob(os.path.join(input_folder, "*.jpg")))
    print(f"{len(image_paths)} 枚の画像を検出")
    
    # 画像がない場合はエラー
    if not image_paths:
        print("エラー: 画像が見つかりませんでした。")
        return
    
    # 画像を開いてリサイズ（透明画像対応のためRGBに変換）
    images = [Image.open(img).convert("RGB").resize(img_size) for img in image_paths]
    
    # 出力画像のサイズを計算
    out_width = img_size[0] * grid_size[0]
    out_height = img_size[1] * grid_size[1]
    
    # 出力用のキャンバスを作成（背景は白）
    output_image = Image.new("RGB", (out_width, out_height), (255, 255, 255))
    
    # 画像を並べる
    for i, img in enumerate(images):
        x = (i % grid_size[0]) * img_size[0]
        y = (i // grid_size[0]) * img_size[1]
        output_image.paste(img, (x, y))
        print(f"画像 {i+1} を ({x}, {y}) に配置")
    
    # 出力フォルダを作成（存在しない場合）
    os.makedirs(output_folder, exist_ok=True)
    
    # 画像を保存
    output_path = os.path.join(output_folder, output_filename)
    output_image.save(output_path)
    print(f"画像を {output_path} に保存しました。")

if __name__ == "__main__":
    combine_images("result", "result1", "face_add.png")
