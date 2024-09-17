---
marp: true
theme: gaia
size: 16:9
paginate: true
header: sola project 2024/9/17
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
 - 設定ファイルの構成を変更

`main.py`の上部にて指定していたパラメータが`params_comfy.json`に移動しました。

# 使用方法
```
python3 main.py (params_comfy.json)
```
実行時引数としてパラメータのjsonのパスを要求します。

# 設定すべき項目

 - `endpoints.py`: エンドポイントの指定
 - `params_comfy.json`: 素材フォルダ、生成フローの指定、パラメータの設定

`params_comfy.json` が通常ワークフローの例です。
`params_comfy_by_character.json`がキャラ別生成フローの例です。

# パラメータファイルについて


```
{
    "material_folder": "test", # 素材のフォルダ
    "user_name": "lovemachine", # ユーザー名（任意）
    "job_name": "test", # ジョブ名（任意）
    "output_path": "test.gif" # 動画を保存したいパス

    "workflow_name": "by_character",
    "parameters":{　
```




`"workflow_name"`にてワークフローの指定が行えます。`"dafault"`または `"by_character"`を指定してください。

# 以下前回から変わらない点

# 環境構築
```
git clone https://github.com/YutoGCN/deploy-demo

cd deploy-demo

pip3 install -r requirements.txt
```

# エンドポイントの設定

```
BASE_URL = ""
```

`endopoint.py`の`""`の間にお渡ししたエンドポイントのurlを入れてください。

# 各種パラメータの説明(1)
通常ワークフローでは3種、キャラ別生成フローでは1種のLoraを指定できます。
`PARAM_LORA_x_NAME` にて `"angel\\\\angel_man_test00.safetensors"` か `"angel\\\\angel_woman_test01-000120.safetensors"`のどちらかを指定してください。
`PARAM_LORA_x_STRENGTH`はLoraの強さで、0.0から1.0の値です。
Loraを適用しない場合は`PARAM_LORA_x_STRENGTH`を0.0としてください。

# 各種パラメータの説明(2)
`"PARAM_PROMPT"`にはプロンプトの文字列を入れてください。

`"PARAM_UPSCALE"`は0.7から1.0の値にしてください。

`"PARAM_DENOISE"`は0.0から1.0の値にしてください。

# 各種パラメータの説明(3)
`"PARAM_CONTROLNET_x_STRENGTH"`はcontrolnetの強さです。それぞれの適用先は以下です。

`"PARAM_CONTROLNET_1_STRENGTH"`: control_v11p_sd15s2_lineart_anime_fp16.safetensors
`"PARAM_CONTROLNET_2_STRENGTH"`: lightingBasedPicture_v10.safetensors
`"PARAM_CONTROLNET_3_STRENGTH"`: control_v11f1e_sd15_tile_fp16.safetensors

# `main.py` の実行

```
python main.py (params_comfy.json)
```

以下が順に実行されます。待機/実行中にCtrl+Cすることでジョブを停止させることができます。`main.py`も同時に終了します。
 - ジョブの投入
 - 待ちがある場合待機
 - 実行（進捗が表示されます）
 - ダウンロード




