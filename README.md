# 臭戯王
サポーターズハッカソンvol_12
## ゲーム概要

ユーザーの臭いの強さを戦闘力として戦うオンラインゲームです。

このリポジトリはクライアント側のコードになります。
Arduinoと臭気センサ(TGS2450)、pythonの実行環境が必要になります。

## 使い方

1. git cloneを行いリポジトリのクローンを作成
2. Pipfile.lockを用いてライブラリのインストール
3. Shugiou-Client内のsketch_dec21a.inoをArduinoに書き込む
4. 臭気センサとArduinoを繋ぐ
5. main.pyを実行

## インストール

```
$ git clone https://github.com/Chaha1n/Shugiou-Client.git
$ cd Shugiou-Client
$ pipenv sync
$ pipenv shell
$ python3 main.py
```

