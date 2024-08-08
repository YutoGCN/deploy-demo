---
marp: true
theme: gaia
size: 16:9
paginate: true
header: sola project 2024/8/8
footer: © 2024 Love Machine Inc.
---
<!--
headingDivider: 1
-->

# sola project demo
<!--
_class: lead
_paginate: false
_header: ""
-->

# 今回の変更点
 - png以外を無視することでmacOSの生成ファイルを無視
 - json decodeの失敗時、再試行することで通信エラーに対処
 - 進捗表示機能を追加
 - 中断機能を追加

以前のクライアントコードは使用しないようお願いいたします。

# 環境構築
```
git clone https://github.com/YutoGCN/deploy-demo

cd deploy-demo

pip3 install -r requirements.txt
```

# `main.py` の設定

`main.py`の上部に設定を行う部分があります。

```
parameters = {
    "material_folder": "test", # 素材のフォルダ
    "user_name": "lovemachine", # ユーザー名（任意）
    "job_name": "test", # ジョブ名（任意）
    "params_comfy_path": "params_comfy.json", # パラメーターファイルのパス
    "output_path": "test.mp4" # 動画を保存したいパス
}
```

パラメーターファイルは動画生成の設定を行うファイルです。

# エンドポイントの設定

```
BASE_URL = ""
```

`endopoint.py`の`""`の間にお渡ししたエンドポイントのurlを入れてください。

# パラメータファイルについて

`params_comfy.json` が例です。`"PARAM_PROMPT"`にはプロンプトの文字列を入れてください。

`PARAM_LORA_x_NAME` は `"angel\\\\angel_man_test00.safetensors"` か `"angel\\\\angel_woman_test01-000120.safetensors"`のどちらかを指定してください。

`"PARAM_UPSCALE"`は0.7から1.0の値にしてください。
その他の数値は0.0から1.0の値にしてください。`PARAM_LORA_x_STRENGTH`はLoraの強さで、0にするとLoraがない状態になります。

# `main.py` の実行

```
python main.py
```

以下が順に実行されます。待機/実行中にCtrl+Cすることでジョブを停止させることができます。`main.py`も同時に終了します。
 - ジョブの投入
 - 待ちがある場合待機
 - 実行（進捗が表示されます）
 - ダウンロード




