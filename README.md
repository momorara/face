# 顔識別のためのリポジトリです。


顔識別のライブラリ(face_recognition)は　2017年3月 に Adam Geitgey氏 によって最初に公開されました。公開された当初、Pythonで簡単に高精度な顔認識ができるということで、大きな反響を呼びました。<br>
ただし、当時のラズパイは　RaspberryPi3B の時代で、ラズパイで実用的なスピードは出せませんでした。また、データセットが欧米人中心だったので、日本人とくに若い女性や子供に対する精度はイマイチとの評価でした。<br>

しかし、Pi5が発売された現在はそこそこ実用的なスピードで処理ができること、昨年(2024年)日本人による日本人の顔データを含んだデータが公開され日本人に対する精度が向上したことから、日本での実用的な使い方が安価なラズパイで実現できるようになってきました。<br>
設定にもよりますが、10FPS程度のスピードで顔判別・識別まで可能です。<br>

<h4><<ライセンスについて >></h4>
今回以下のリポジトリを参考にしています。<br>
https://github.com/ageitgey/face_recognition<br>
https://github.com/davisking/dlib-models<br>
https://github.com/TaguchiModels/dlibModels<br>
ライセンスとしてそれぞれのライセンスを掲示しています。<br>
オリジナル部分もそれぞれに準じます。<br>

<h4><<テストデータ>></h4>
実際の人間の顔をカメラで撮影してデータとできれば良かったのですが、人数を集められないので、フリー素材の写真で代用しています。
子供から老人までの49人分の写真をカメラで撮影して、その写真の識別を行いました。元データと同じ写真ではあるものの100%の正解でした。
Pi4Bで5FPS、Pi5で10FPSのスピードでしたので、まずまず実用耐えるのではと考えています。<br>
<img src="https://github.com/user-attachments/assets/43bf156e-a373-4364-bb0b-c8b3c75f9627" width="500">
  
<img src="https://github.com/user-attachments/assets/0448c8f3-1af0-45bd-ae7c-10d20c7ac119" width="500"><br>

<img src="https://github.com/user-attachments/assets/a9ab521d-1e3d-46dc-916e-40e94d80da74" width="500"><br>

<h4><<使用方法>></h4>
購入者にはインストール済みのmicroSDをmicroSDを提供しています。プログラムにアップデートが必要な場合のみインストールしてください。<br>
git clone https://github.com/momorara/face<br>
にて、パソコンに一括ダウンロード可能です。<br>
<br>
おまけのyoloについては、ライセンスを読んだ上でインストールしてください。<br>


<h4><<動作環境>></h4>
Pi5、Pi4Bで Bookworm 32bit、64bit(Pi5/64bit推奨) で動作しました。

<h4><<使用説明資料>></h4>
説明書類の中の資料を確認ください。
お問い合わせに関しては、購入ページからお願いします。　

<h4><<メンテナンス情報>></h4>
現在作成中

<h4><<サポート窓口>></h4>
  メールアドレスが　tkj-works@mbr.nifty.com に変更になっています。<br>
  資料等を修正中ですが、ご注意ください。<br>
  サポートコミュニティー　https://www.facebook.com/groups/3773038759434230<br>
