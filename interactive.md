---
marp: true
theme: gaia
size: 16:9
paginate: true
header: sola project 2024/9/24
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
 - 対話的な進捗確認・ダウンロードのためのツールの追加

# 対話的ツールの使い方

```
python3 interactive.py (params_comfy.json)
```

`params_comfy.json`は`main.py`のものと同じものをお使いください

# モード一覧

対話的に以下を行えます
・mode 1: 生成リクエスト
・mode 2: ユーザーの投げたジョブ一覧の取得
・mode 3: ジョブの進捗確認
・mode 4: 生成結果をダウンロード
・mode 5: 中断

プログラムを起動するとモードを聞かれ、モードによっては次に`run_id`を聞かれます。適宜入力をお願いいたします。