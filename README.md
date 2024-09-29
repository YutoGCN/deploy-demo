---
marp: true
theme: gaia
size: 16:9
paginate: true
header: sola project 2024/9/30
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
 - 部分ControlNetフローに対応
 - BaseModelを変更可能に
 - 生成ファイルのフォーマットを動画ファイルから`.png`に変更

以前のクライアントコードは使用しないようお願いいたします。また、エンドポイントが変更となりました。

# 環境構築
```
git clone https://github.com/YutoGCN/deploy-demo

cd deploy-demo

pip3 install -r requirements.txt
```

# 設定すべき項目
 - `endpoints.py`: エンドポイントの指定
 - `params_comfy.json`: 生成フローの指定、パラメータの設定

パラメータファイルについて、`params_comfy.json`,`params_comfy_by_character.json`,`params_comfy_PartialCN-Chara.json`がサンプルです。

# 入力・出力等の設定

```
{
    "material_folder": "test",
    "user_name": "lovemachine",
    "job_name": "dafult_20240929",
    "output_path": "output/test",
```

出力が`.png`になったことにより、出力の指定がディレクトリになりました。

# ワークフローの指定

```
    "workflow_name": "dafault",
```
`dafult`,`by_character`,`PartialCN-Chara`のいずれかを使用してください。それぞれ通常ワークフロー、キャラ別生成フロー、部分ControlNetフローです。

# ベースモデルの指定
すべてのワークフローにおいて、ベースモデルの指定が可能です。
```
    "parameters":{
        "PARAM_BASEMODEL": "animelike25D_animelike25DV11Pruned.safetensors",
```
`"animelike25D_animelike25DV11Pruned.safetensors"`または`"cetusMix_Whalefall2.safetensors"`をご使用ください。

# マスクの設定ついて
部分ControlNetフローについて、マスクの指定が必要です。
```
        "PARAM_MASK_PROMPT": "",
        "PARAM_MASK_OBJECT_PROMPT": "face",
```
`"PARAM_MASK_PROMPT"`にはマスク部分に適用するプロンプトをいれてください。`"PARAM_MASK_OBJECT_PROMPT"`にはマスクを適用したい部位に対するプロンプトをいれてください。

# ControlNetの設定
部分ControlNetフローについて、LINEARTとTILEについて、マスク内・マスク外それぞれに対し、強度を指定できます。LIGHTBASEDPICTUREは適用できません。

```
        "PARAM_CONTROLNET_LINEART_WITH_MASK_STRENGTH": 0.8,
        "PARAM_CONTROLNET_LINEART_OUT_MASK_STRENGTH": 0.4,
        "PARAM_CONTROLNET_LIGHTBASEDPICTURE_STRENGTH": 0.4,
        "PARAM_CONTROLNET_TILE_WITH_MASK_STRENGTH": 0.6,
        "PARAM_CONTROLNET_TILE_OUT_MASK_STRENGTH": 0.4
```

# 以下前回から変更のない部分

# エンドポイントの設定

```
BASE_URL = ""
```

`endopoint.py`の`""`の間にお渡ししたエンドポイントのurlを入れてください。

# 各種パラメータの説明(1)
通常ワークフローでは3種、キャラ別生成フロー・部分コントロールネットフローでは1種のLoraを指定できます。
`PARAM_LORA_x_NAME` にて `"angel\\\\angel_man_test00.safetensors"` か `"angel\\\\angel_woman_test01-000120.safetensors"`のどちらかを指定してください。
`PARAM_LORA_x_STRENGTH`はLoraの強さで、0.0から1.0の値です。
Loraを適用しない場合は`PARAM_LORA_x_STRENGTH`を0.0としてください。

# 各種パラメータの説明(2)
`"PARAM_PROMPT"`にはプロンプトの文字列を入れてください。

`"PARAM_UPSCALE"`は0.7から1.0の値にしてください。大きい値にするほど生成時の解像度が向上します。（生成時間も長くなります）

`"PARAM_DENOISE"`は0.0から1.0の値にしてください。

# 各種パラメータの説明(3)
通常ワークフローでは3種、キャラ別生成フローにおけるControlNetの説明です。
`"PARAM_CONTROLNET_x_STRENGTH"`はcontrolnetの強さです。それぞれの適用先は以下です。

`"PARAM_CONTROLNET_1_STRENGTH"`: control_v11p_sd15s2_lineart_anime_fp16.safetensors
`"PARAM_CONTROLNET_2_STRENGTH"`: lightingBasedPicture_v10.safetensors
`"PARAM_CONTROLNET_3_STRENGTH"`: control_v11f1e_sd15_tile_fp16.safetensors

# `main.py` の実行

```
python main.py
```

以下が順に実行されます。待機/実行中にCtrl+Cすることでジョブを停止させることができます。`main.py`も同時に終了します。
 - ジョブの投入
 - 待ちがある場合待機
 - 実行（進捗が表示されます）
 - ダウンロード




